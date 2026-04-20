"""
Parser for extracting data from the report template
"""
import re
from datetime import datetime
from typing import Optional, Dict, List


class ReportParser:
    """Parse intern reports from text messages"""

    @staticmethod
    def parse_report(text: str) -> Optional[Dict]:
        """
        Parse report template and extract data
        
        Expected format:
        #hisobot
        👤 Intern: [Ism Familiya]
        📅 Sana: DD.MM.YYYY
        
        🕒 ISH VAQTI:
        📥 Kelgan: HH:MM
        📤 Ketgan: HH:MM
        
        📚 DARSLAR JADVALI:
        
        🔹 Dars #1
        ┣ 👨‍🏫 Ustoz: [Name]
        ┣ 🚪 Xona: [Room]
        ┗ ⏰ Vaqt: HH:MM
        
        ... and so on
        """
        
        lines = text.strip().split('\n')
        data = {
            'intern_name': None,
            'date': None,
            'arrival_time': None,
            'departure_time': None,
            'lessons': [],
            'raw_text': text
        }
        
        # Parse intern name
        intern_match = re.search(r'👤\s*Intern:\s*(.+?)(?:\n|$)', text)
        if intern_match:
            name = intern_match.group(1).strip()
            # Remove brackets if present (e.g., [Ism Familiya] -> Ism Familiya)
            name = re.sub(r'^\[|\]$', '', name).strip()
            data['intern_name'] = name
        
        # Parse date
        date_match = re.search(r'📅\s*Sana:\s*(\d{1,2}\.\d{1,2}\.\d{4})', text)
        if date_match:
            date_str = date_match.group(1).strip()
            try:
                data['date'] = datetime.strptime(date_str, '%d.%m.%Y').date()
            except ValueError:
                data['date'] = None
        
        # Parse arrival time
        arrival_match = re.search(r'📥\s*Kelgan:\s*(\d{1,2}:\d{2})', text)
        if arrival_match:
            data['arrival_time'] = arrival_match.group(1).strip()
        
        # Parse departure time
        departure_match = re.search(r'📤\s*Ketgan:\s*(\d{1,2}:\d{2})', text)
        if departure_match:
            data['departure_time'] = departure_match.group(1).strip()
        
        # Parse lessons
        lessons = []
        # Look for lesson patterns with various emoji formats
        lesson_pattern = r'🔹\s*Dars\s*#(\d+)(.*?)(?=🔹|$)'
        matches = re.finditer(lesson_pattern, text, re.DOTALL)
        
        for match in matches:
            lesson_num = match.group(1)
            lesson_text = match.group(2)
            
            # Match teacher - look for "Ustoz:" pattern regardless of emoji variation
            teacher_match = re.search(r'Ustoz:\s*([^\n┣]*)', lesson_text)
            # Match room
            room_match = re.search(r'Xona:\s*([^\n┣]*)', lesson_text)
            # Match time
            time_match = re.search(r'Vaqt:\s*(\d{1,2}:\d{2})', lesson_text)
            
            teacher = teacher_match.group(1).strip() if teacher_match else ''
            room = room_match.group(1).strip() if room_match else ''
            time_val = time_match.group(1).strip() if time_match else ''
            
            # Remove brackets if present (e.g., [Name] -> Name)
            teacher = re.sub(r'^\[|\]$', '', teacher).strip()
            room = re.sub(r'^\[|\]$', '', room).strip()
            
            # Only add lesson if it has both teacher and time
            if teacher and time_val:
                lesson = {
                    'number': lesson_num,
                    'teacher': teacher,
                    'room': room,
                    'time': time_val
                }
                lessons.append(lesson)
        
        data['lessons'] = lessons
        
        return data if ReportParser.validate_report(data) else None

    @staticmethod
    def validate_report(data: Dict) -> bool:
        """Validate parsed report data"""
        
        # For absence reports, skip validation
        if data.get('status') == 'Kelmadi':
            return bool(data.get('intern_name') and data.get('absence_reason'))
        
        # Check required fields for attendance reports
        required_fields = ['intern_name', 'date', 'arrival_time', 'departure_time']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        # Check time format
        time_pattern = r'^\d{1,2}:\d{2}$'
        if not re.match(time_pattern, data['arrival_time']):
            return False
        if not re.match(time_pattern, data['departure_time']):
            return False
        
        # Check at least one lesson
        if not data.get('lessons') or len(data['lessons']) == 0:
            return False
        
        # Check lesson data - teacher must not be empty
        for lesson in data['lessons']:
            teacher = lesson.get('teacher', '').strip()
            time_val = lesson.get('time', '').strip()
            if not teacher or not time_val:
                return False
        
        return True

    @staticmethod
    def get_error_message(data: Dict) -> str:
        """Get specific error message based on validation"""
        
        if not data.get('intern_name'):
            return "❌ Intern nomi topilmadi. (👤 Intern: [Ism Familiya])"
        
        if not data.get('date'):
            return "❌ Sana noto'g'ri formatda. (📅 Sana: DD.MM.YYYY)"
        
        if not data.get('arrival_time') or not data.get('departure_time'):
            return "❌ Kelgan yoki ketgan vaqti topilmadi."
        
        if not data.get('lessons'):
            return "❌ Darslar ro'yxati bo'sh. Kamida bitta dars qo'shing."
        
        for i, lesson in enumerate(data['lessons'], 1):
            if not lesson.get('teacher'):
                return f"❌ Dars #{i}: Ustoz nomi topilmadi."
            if not lesson.get('time'):
                return f"❌ Dars #{i}: Vaqti topilmadi."
        
        return "❌ Shablonda xatolik bor. Iltimos qayta urinib ko'ring."


class TemplateGenerator:
    """Generate report template"""

    @staticmethod
    def generate_template() -> str:
        """Generate default report template"""
        return """#hisobot
👤 Intern: [Ism Familiya]
📅 Sana: 15.03.2026

🕒 ISH VAQTI:
📥 Kelgan: 09:50
📤 Ketgan: 16:20
━━━━━━━━━━━━━━━━━━

📚 DARSLAR JADVALI:

🔹 Dars #1
┣ 👨‍🏫 Ustoz: Ustoz1
┣ 🚪 Xona: B8-xona
┗ ⏰ Vaqt: 10:10

🔹 Dars #2
┣ 👨‍🏫 Ustoz: Ustoz2
┣ 🚪 Xona: A3-xona
┗ ⏰ Vaqt: 15:10"""
