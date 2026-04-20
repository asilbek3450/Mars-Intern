"""
Bot handlers for processing user messages and commands
"""
from datetime import date, datetime
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from states import InternForm, WorkSession
from parser import ReportParser, TemplateGenerator
from database import db
from keyboards import (
    get_main_keyboard,
    get_intern_selection_keyboard,
    get_cancel_keyboard,
    get_yes_no_keyboard
)
from config import (
    BTN_DARS_KIRITISH,
    BTN_CANCEL,
    MSG_WELCOME,
    MSG_SELECT_INTERNSHIP,
    MSG_TEMPLATE_REQUEST,
    MSG_TEMPLATE_ERROR,
    MSG_SUCCESS,
    MSG_ABSENCE
)
from interns import INTERNS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await message.answer(
        MSG_WELCOME,
        reply_markup=get_main_keyboard()
    )
    await state.clear()


@router.message(F.text == "🟢 Ish boshladim")
async def start_work_session(message: Message, state: FSMContext):
    """Handle work session start"""
    interns_list = ", ".join(INTERNS)
    await message.answer(
        f"👤 Qaysi intern ish boshlamoqda?\n\n"
        f"Mavjud interns:\n{interns_list}\n\n"
        f"Ismini yozing:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(WorkSession.selecting_intern_start)


@router.message(F.text == "🔴 Ish tugatim")
async def end_work_session_request(message: Message, state: FSMContext):
    """Handle work session end request"""
    interns_list = ", ".join(INTERNS)
    await message.answer(
        f"👤 Qaysi intern ish tugatmoqda?\n\n"
        f"Mavjud interns:\n{interns_list}\n\n"
        f"Ismini yozing:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(WorkSession.selecting_intern_end)


@router.message(WorkSession.selecting_intern_start, F.text.in_(INTERNS))
async def handle_work_intern_start(message: Message, state: FSMContext):
    """Handle intern selection for work session start"""
    intern_name = message.text
    
    # Check if already has active session
    active_session = db.get_work_session(intern_name)
    
    if active_session:
        await message.answer(
            f"⚠️ {intern_name} allaqachon ish boshlagani mavjud\n"
            f"🕐 Boshlanish: {active_session['start_time'][:5]}\n\n"
            f"Ish tugatish uchun '🔴 Ish tugatim' ni bosing.",
            reply_markup=get_main_keyboard()
        )
    else:
        # Start the session
        if db.start_work_session(intern_name):
            await message.answer(
                f"🟢 Ish boshlandi!\n\n"
                f"👤 {intern_name}\n"
                f"⏰ Vaqt: {datetime.now().strftime('%H:%M:%S')}\n\n"
                f"Ish tugatish uchun '🔴 Ish tugatim' ni bosing.",
                reply_markup=get_main_keyboard()
            )
            db.add_log(message.from_user.id, "work_session_started", f"{intern_name}")
        else:
            await message.answer(
                "❌ Xato: Ish boshlanmadi",
                reply_markup=get_main_keyboard()
            )
    
    await state.clear()


@router.message(WorkSession.selecting_intern_end, F.text.in_(INTERNS))
async def handle_work_intern_end(message: Message, state: FSMContext):
    """Handle intern selection for work session end"""
    intern_name = message.text
    
    active_session = db.get_work_session(intern_name)
    
    if active_session:
        # End the session
        if db.end_work_session(intern_name):
            start_time = datetime.fromisoformat(active_session['start_time'])
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds() / 60)
            hours = duration // 60
            minutes = duration % 60
            
            await message.answer(
                f"✅ Ish tugatildi!\n\n"
                f"👤 {intern_name}\n"
                f"⏱️ Ish vaqti: {hours}h {minutes}m ({duration} min)\n"
                f"🕐 Boshlanish: {start_time.strftime('%H:%M:%S')}\n"
                f"🕐 Tugash: {end_time.strftime('%H:%M:%S')}",
                reply_markup=get_main_keyboard()
            )
            db.add_log(message.from_user.id, "work_session_ended", f"{intern_name}: {duration}min")
        else:
            await message.answer(
                "❌ Xato: Ish tugatilmadi",
                reply_markup=get_main_keyboard()
            )
    else:
        await message.answer(
            f"❌ {intern_name} uchun faol ish sessiyasi topilmadi",
            reply_markup=get_main_keyboard()
        )
    
    await state.clear()


@router.message(WorkSession.selecting_intern_start, F.text == BTN_CANCEL)
@router.message(WorkSession.selecting_intern_end, F.text == BTN_CANCEL)
async def cancel_work_selection(message: Message, state: FSMContext):
    """Cancel work session selection"""
    await message.answer(
        "Bekor qilindi.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


@router.message(F.text == BTN_DARS_KIRITISH)
async def btn_dars_kiritish(message: Message, state: FSMContext):
    """Handle 'Dars kiritish' button - ask user to select name"""
    await message.answer(
        MSG_SELECT_INTERNSHIP,
        reply_markup=get_intern_selection_keyboard()
    )
    await state.set_state(InternForm.selecting_name)


@router.message(InternForm.selecting_name, F.text == BTN_CANCEL)
async def cancel_selection(message: Message, state: FSMContext):
    """Cancel name selection"""
    await message.answer(
        "Bekor qilindi. Bosh menyudan boshlang.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


@router.message(InternForm.selecting_name, F.text.in_(INTERNS))
async def select_intern(message: Message, state: FSMContext):
    """Handle intern name selection"""
    intern_name = message.text
    
    await state.update_data(intern_name=intern_name)
    await state.set_state(InternForm.waiting_for_report)
    
    template = TemplateGenerator.generate_template()
    
    await message.answer(
        f"Tanlandi: {intern_name}\n\n"
        f"Shu shablonni to'ldirib yuboring:\n\n"
        f"<code>{template}</code>\n\n"
        f"{MSG_TEMPLATE_REQUEST}",
        reply_markup=get_cancel_keyboard()
    )


@router.message(InternForm.selecting_name)
async def invalid_selection(message: Message, state: FSMContext):
    """Handle invalid name selection"""
    await message.answer(
        "❌ Iltimos, ro'yxatdan birini tanlang yoki '❌ Bekor qilish' tugmasini bosing.",
        reply_markup=get_intern_selection_keyboard()
    )


@router.message(InternForm.waiting_for_report, F.text == BTN_CANCEL)
async def cancel_report(message: Message, state: FSMContext):
    """Cancel report submission"""
    await message.answer(
        "Bekor qilindi. Bosh menyudan boshlang.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


@router.message(InternForm.waiting_for_report)
async def process_report(message: Message, state: FSMContext):
    """Process submitted report"""
    text = message.text
    
    # Check if message starts with #hisobot
    if '#hisobot' not in text.lower():
        await message.answer(
            "❌ Shablonni topilmadi. '#hisobot' bilan boshlang.",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    # Parse report
    parsed_data = ReportParser.parse_report(text)
    
    if not parsed_data:
        error_msg = ReportParser.get_error_message(parsed_data if parsed_data else {})
        await message.answer(
            f"❌ Xato: {error_msg}\n\n{MSG_TEMPLATE_REQUEST}",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    # Get stored intern name
    data = await state.get_data()
    stored_intern_name = data.get('intern_name')
    
    # Verify intern name matches
    if parsed_data['intern_name'] != stored_intern_name:
        await message.answer(
            f"❌ Tanlovangiz: {stored_intern_name}\n"
            f"Shaklondagi: {parsed_data['intern_name']}\n\n"
            f"Nomlar mos kelmadi. Qayta urinib ko'ring.",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    # Store parsed data in state
    parsed_data['status'] = 'Keldi'
    await state.update_data(parsed_report=parsed_data)
    await state.set_state(InternForm.confirming_report)
    
    # Show confirmation
    lesson_list = '\n'.join([
        f"  🔹 Dars #{lesson['number']}: {lesson['teacher']} ({lesson['time']})"
        for lesson in parsed_data['lessons']
    ])
    
    confirmation_text = (
        f"✅ Hisobot tahlili qabul qilindi!\n\n"
        f"👤 Intern: {parsed_data['intern_name']}\n"
        f"📅 Sana: {parsed_data['date'].strftime('%d.%m.%Y')}\n"
        f"🕒 Kelgan: {parsed_data['arrival_time']}\n"
        f"🕒 Ketgan: {parsed_data['departure_time']}\n"
        f"📚 Darslar ({len(parsed_data['lessons'])} ta):\n"
        f"{lesson_list}\n\n"
        f"To'g'rimi?"
    )
    
    await message.answer(
        confirmation_text,
        reply_markup=get_yes_no_keyboard()
    )


@router.message(InternForm.confirming_report, F.text == "✅ Ha")
async def confirm_report(message: Message, state: FSMContext):
    """Confirm and save report"""
    data = await state.get_data()
    parsed_report = data.get('parsed_report')
    
    if not parsed_report:
        await message.answer(
            "❌ Hisobot ma'lumotlari yo'q. Qayta boshlang.",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        return
    
    # Debug print
    print(f"📝 Saving report: {parsed_report}")
    
    # Save to database
    success = db.add_report(parsed_report)
    
    if success:
        await message.answer(
            f"{MSG_SUCCESS}\n\n"
            f"Rahmat, {parsed_report['intern_name']}!",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "❌ Database xatosi. Admin bilan bog'laning.",
            reply_markup=get_main_keyboard()
        )
    
    await state.clear()


@router.message(InternForm.confirming_report, F.text == "❌ Yo'q")
async def reject_report(message: Message, state: FSMContext):
    """Reject and re-submit"""
    data = await state.get_data()
    stored_intern_name = data.get('intern_name')
    
    template = TemplateGenerator.generate_template()
    
    await message.answer(
        f"Qaytadan to'ldirib yuboring:\n\n"
        f"<code>{template}</code>\n\n"
        f"{MSG_TEMPLATE_REQUEST}",
        reply_markup=get_cancel_keyboard()
    )
    
    await state.set_state(InternForm.waiting_for_report)


@router.message(InternForm.waiting_for_absence_reason)
async def process_absence_reason(message: Message, state: FSMContext):
    """Process absence reason"""
    reason = message.text
    
    data = await state.get_data()
    intern_name = data.get('intern_name')
    
    absence_data = {
        'intern_name': intern_name,
        'date': date.today(),
        'arrival_time': '',
        'departure_time': '',
        'lessons': [],
        'status': 'Kelmadi',
        'absence_reason': reason
    }
    
    db.add_report(absence_data)
    
    await message.answer(
        f"✅ Qayd qilindi: {intern_name} kelmadi. Sabab: {reason}",
        reply_markup=get_main_keyboard()
    )
    
    await state.clear()


@router.message()
async def echo(message: Message):
    """Echo unknown messages"""
    await message.answer(
        "❌ Noto'g'ri buyruq.\n\n"
        "Bosh menyudan tanlang:",
        reply_markup=get_main_keyboard()
    )
