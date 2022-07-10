from aiogram.utils.markdown import hbold as bold, hlink as link


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


about_bot = f"<i><b>Пишет @karych.</b>\n\n" \
            f"На самом деле, бот создан за пару часов по-приколу и идейно не рассчитан на " \
            f"большой спрос. Это скорее пет-проект для души и для практики моих навыков.\n\n" \
            f"Исходники лежат {link(title='тут', url='github.com/devkarych/notify-bot')}. " \
            f"Если ты увлекаешься ITшкой, то можешь чекнуть мой бложик (я туда " \
            f"переодически пишу для души).\nНу и личка всегда открыта для " \
            f"твоих предложений и идей =)</i>"
