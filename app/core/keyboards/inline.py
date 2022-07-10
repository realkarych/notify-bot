from aiogram.types import InlineKeyboardMarkup

from app.core.navigations import inline
from app.core.navigations.inline import InlineCallback

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            inline.cancel.to_inline_button()
        ]
    ]
)


def hours() -> InlineKeyboardMarkup:
    """Returns hours markup with 4 lines & 6 line-len"""

    return _build_time_markup(line_len=6, lines_count=4, buttons=inline.hours)


def minutes() -> InlineKeyboardMarkup:
    """Returns minutes (%5 == 0) markup"""

    return _build_time_markup(line_len=4, lines_count=3, buttons=inline.minutes)


def _build_time_markup(
        line_len: int,
        lines_count: int,
        buttons: list[InlineCallback]
) -> InlineKeyboardMarkup:
    btns_counter = 0
    keyboard = []

    for cur_line in range(lines_count):
        keyboard.append([])
        for cur_btn in range(line_len):
            keyboard[cur_line].append(buttons[btns_counter].to_inline_button())
            btns_counter += 1

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
