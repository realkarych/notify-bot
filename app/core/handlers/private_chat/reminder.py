import asyncio
import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ChatActions

from app.core.keyboards import reply, inline
from app.core.keyboards.calendar import Calendar, calendar_callback
from app.core.messages.private_chat import reminder as msgs
from app.core.middlewares.throttling import throttle
from app.core.navigations import reply as reply_nav
from app.core.navigations.reply import cancel
from app.core.states.reminder import ReminderAddition
from app.models.dto import Reminder
from app.services.database.dao.reminder import ReminderDAO


async def btn_cancel(m: types.Message, state: FSMContext):
    """Universal canceller from any state"""

    await m.reply("<b>Отмена!</b>", reply_markup=reply.default)
    await state.finish()


@throttle(limit=2)
async def btn_add_reminder(m: types.Message):
    """Add reminder command handling"""

    await m.answer(msgs.enter_reminder_text, reply_markup=reply.cancel)
    await ReminderAddition.text.set()


@throttle(limit=2)
async def state_submit_reminder(m: types.Message, state: FSMContext):
    """Adds reminder text to memory storage"""

    async with state.proxy() as data:
        data['reminder'] = m.parse_entities()

    await m.reply(msgs.set_time_on_calendar, reply_markup=await Calendar().start_calendar())
    await ReminderAddition.date.set()


async def calendar_process(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """Calendar date choosing process"""

    selected, date = await Calendar().process_selection(call, callback_data)
    if selected:
        async with state.proxy() as data:
            data['date']: datetime.datetime = date
            await call.message.edit_text(msgs.set_hours(submitted_date=date))
            await call.message.edit_reply_markup(inline.hours())

        await ReminderAddition.hours.set()


async def submit_hours(call: CallbackQuery, state: FSMContext):
    """User submitted the hour by inl button click"""

    async with state.proxy() as data:
        submitted_hour = int(call.data.replace("hour_", ""))
        data['date'] = data['date'].replace(hour=submitted_hour)

        await call.message.edit_text(msgs.set_minutes(data['date']))
        await call.message.edit_reply_markup(inline.minutes())

    await ReminderAddition.minutes.set()


async def submit_minutes(call: CallbackQuery, state: FSMContext):
    """User submitted the minute by inl button click"""

    await call.message.edit_reply_markup(None)

    async with state.proxy() as data:
        submitted_minute = int(call.data.replace("minute_", ""))
        # Now, date is ready
        data['date'] = data['date'].replace(minute=submitted_minute)

        # Check if date is in the future
        if datetime.datetime.now() < data['date']:
            await call.message.edit_text(msgs.reminder_created(data['date']))

            # Adding reminder to database
            await ReminderDAO(session=call.bot.get("db")).add_reminder(
                reminder=Reminder(
                    owner_id=call.from_user.id,
                    notify_time=data['date'],
                    text=data['reminder']
                ))
        # Date is missed
        else:
            await call.message.edit_text(msgs.date_missed(submitted_date=data['date']))

    await call.message.answer_chat_action(ChatActions.TYPING)
    await asyncio.sleep(1)
    await call.message.answer(msgs.return_to_default_menu, reply_markup=reply.default)
    await state.finish()


def register_handlers(dp: Dispatcher) -> None:
    """Register handlers for reminders interaction (addition, deletion, list-printing etc.)"""

    dp.register_message_handler(btn_add_reminder, Text(equals=[reply_nav.add_reminder]))
    dp.register_message_handler(btn_cancel, Text(equals=[cancel]), state="*")
    dp.register_callback_query_handler(calendar_process, calendar_callback.filter(),
                                       state=ReminderAddition.date)
    dp.register_message_handler(state_submit_reminder, state=ReminderAddition.text)
    dp.register_callback_query_handler(submit_hours, state=ReminderAddition.hours)
    dp.register_callback_query_handler(submit_minutes, state=ReminderAddition.minutes)
