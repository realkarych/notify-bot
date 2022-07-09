from aiogram.utils.markdown import hbold as bold


def welcome(user_firsname: str) -> str:
    """
    :param user_firsname:
    :return: welcome message to user
    """

    return bold(f'Привет, {user_firsname}!') + \
           f"\n\nСо мной не забудешь, честно. Приятного использования =)\n\n" \
           f"<i>Фана ради запилил <b>@karych</b>.</i>"
