from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup(dispatcher: Dispatcher):
    """
    Setup middlewares with given dispatcher
    :param dispatcher:
    """

    dispatcher.middleware.setup(ThrottlingMiddleware(rate_limit=1))
