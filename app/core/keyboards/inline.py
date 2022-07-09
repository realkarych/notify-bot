from aiogram.types import InlineKeyboardMarkup

from app.core.navigations import inline

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            inline.cancel.to_inline_button()
        ]
    ]
)
