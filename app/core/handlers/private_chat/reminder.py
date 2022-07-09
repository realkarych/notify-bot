from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from app.core.keyboards import reply, inline
from app.core.keyboards.calendar import Calendar, calendar_callback
from app.core.messages.private_chat import reminder as msgs
from app.core.middlewares.throttling import throttle
from app.core.navigations import reply as reply_nav
from app.core.navigations.inline import cancel
from app.core.states.reminder import ReminderAddition


async def btn_cancel(call: types.CallbackQuery, state: FSMContext):
    """Universal canceller from any state"""

    await call.message.edit_reply_markup(None)
    await call.message.reply("<b>Отмена!</b>", reply_markup=reply.default)
    await state.finish()


@throttle(limit=2)
async def btn_add_reminder(m: types.Message):
    """Add reminder command handling"""

    await m.answer(msgs.enter_reminder_text, reply_markup=inline.cancel)
    await ReminderAddition.text.set()


@throttle(limit=2)
async def state_enter_reminder(m: types.Message, state: FSMContext):
    """Adds reminder text to memory storage"""

    async with state.proxy() as data:
        data['reminder'] = m.text

    await state.finish()

    await m.reply(msgs.set_time_on_calendar, reply_markup= await Calendar().start_calendar())


async def calendar_process(callback_query: CallbackQuery, callback_data: dict):
    """Calendar date choosing process"""
    
    selected, date = await Calendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=reply.default
        )


def register_handlers(dp: Dispatcher) -> None:
    """Register handlers for reminders interaction (addition, deletion, list-printing etc.)"""

    dp.register_message_handler(btn_add_reminder, Text(equals=[reply_nav.add_reminder]))
    dp.register_callback_query_handler(btn_cancel, text=cancel.callback, state="*")
    dp.register_callback_query_handler(calendar_process, calendar_callback.filter())
    dp.register_message_handler(state_enter_reminder, state=ReminderAddition.text)
