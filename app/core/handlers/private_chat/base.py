from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.keyboards import reply
from app.core.messages.private_chat import base as msgs
from app.core.middlewares.throttling import throttle
from app.core.navigations import reply as reply_nav
from app.core.navigations.command import Commands
from app.models.dto import get_user_from_message
from app.services.database.dao.reminder import ReminderDAO
from app.services.database.dao.user import UserDAO


@throttle(limit=2)
async def cmd_start(m: types.Message, state: FSMContext):
    """/start command handling"""

    await state.finish()
    user = get_user_from_message(message=m)
    session = UserDAO(session=m.bot.get("db"))
    await session.add_user(user)

    await m.answer(msgs.welcome(user_firstname=user.firstname), reply_markup=reply.default)


@throttle(limit=2)
async def btn_stats(m: types.Message):
    """Displays current bot stats"""

    user_dao = UserDAO(session=m.bot.get("db"))
    rem_dao = ReminderDAO(session=m.bot.get("db"))

    await m.answer(msgs.get_stats(users_count=await user_dao.count(),
                                  reminders_count=await rem_dao.count()))


def register_handlers(dp: Dispatcher) -> None:
    """Register handlers for newcomers"""

    dp.register_message_handler(cmd_start, commands=str(Commands.start), state="*")
    dp.register_message_handler(btn_stats, Text(equals=reply_nav.check_stats))
