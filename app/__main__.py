"""App launcher"""

import asyncio
import logging

import tzlocal
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core import middlewares
from core.handlers.factory import DefaultHandlersFactory
from core.handlers.private_chat import (
    base, reminder
)
from core.navigations.command import set_bot_commands
from core.updates import worker
from services.database.connector import setup_get_pool
from services.reminder.scheduler import setup_notificator
from settings import config as _config


def _init_scheduler() -> AsyncIOScheduler:
    """
    Initialize & start scheduler.
    :return scheduler:
    """
    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
    scheduler.start()
    return scheduler


def _setup_cron_jobs(scheduler: AsyncIOScheduler, bot: Bot) -> None:
    """
    Register jobs (delayed & repeated tasks).
    :param scheduler: initialized instance
    :param bot: Initialized bot instance for sending notifications.
    """

    scheduler.add_job(setup_notificator, IntervalTrigger(minutes=1), (bot,))


async def main() -> None:
    """Starts app & polling."""

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    config: _config.Config = _config.load_config()

    bot = Bot(config.bot.token, parse_mode=config.bot.parse_mode)
    bot["db"] = await setup_get_pool(db_uri=config.db.get_uri())
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    await set_bot_commands(bot=bot)

    # Middlewares setup. Register middlewares provided to __init__.py in middlewares package.
    middlewares.setup(dispatcher=dp)
    # Provide your default handler-modules into register() func.
    DefaultHandlersFactory(dp).register(base, reminder)
    _setup_cron_jobs(scheduler=_init_scheduler(), bot=bot)

    try:
        await dp.start_polling(allowed_updates=worker.get_handled_updates(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Log this is pointless
        pass
