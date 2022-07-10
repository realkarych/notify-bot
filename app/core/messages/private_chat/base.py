from aiogram.utils.markdown import hbold as bold


def welcome(user_firstname: str) -> str:
    """
    :param user_firstname:
    :return: welcome message to user
    """

    return bold(f'Привет, {user_firstname}!') + \
           "\n\nСо мной не забудешь таски закрыть, любимое дело сделать. Главное, " \
           "не выключай уведомления. Приятного использования =)\n\n" \
           "<i>Фана ради запилил <b>@karych</b>.</i>"


def get_stats(users_count: int, reminders_count: int) -> str:
    """Returns bot stats message"""
    return f"<i><b>Статистика:</b>\n\n" \
           f"Пользователей бота: {users_count}.\n" \
           f"Количество активных напоминалок: {reminders_count}.</i>"
