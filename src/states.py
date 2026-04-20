"""
FSM (Finite State Machine) states for the bot
"""
from aiogram.fsm.state import State, StatesGroup


class InternForm(StatesGroup):
    """States for intern report form"""
    selecting_name = State()
    waiting_for_report = State()
    waiting_for_absence_reason = State()
    confirming_report = State()


class WorkSession(StatesGroup):
    """States for work session management"""
    selecting_intern_start = State()
    selecting_intern_end = State()
