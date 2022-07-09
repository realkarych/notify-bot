from aiogram.dispatcher.filters.state import StatesGroup, State


class ReminderAddition(StatesGroup):
    """Reminder completion pipeline"""

    text = State()
    date = State()
