from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.navigations import reply


class ResizedReplyKeyboard(ReplyKeyboardMarkup):
    """
    I prefer override default ReplyKeyboardMarkup to avoid passing the resizer parameter
    every time.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize_keyboard = True


# Markup with default menu buttons
default = ResizedReplyKeyboard(
    keyboard=[
        [
            KeyboardButton(reply.add_reminder)
        ],
        [
            KeyboardButton(reply.reminder_list)
        ],
        [
            KeyboardButton(reply.check_stats),
            KeyboardButton(reply.about_bot)
        ]
    ]
)

# Cancel markup
cancel = ResizedReplyKeyboard(
    keyboard=[
        [KeyboardButton(reply.cancel)]
    ]
)
