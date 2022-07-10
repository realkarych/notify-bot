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
        for _ in range(line_len):
            keyboard[cur_line].append(buttons[btns_counter].to_inline_button())
            btns_counter += 1

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def reminder_params(reminder_id: int) -> InlineKeyboardMarkup:
    """Returns unique reminder-params keyboard"""
    inline_callback = InlineCallback(
        text=inline.delete_reminder.text,
        callback=inline.delete_reminder.callback
    )

    # Update callback from "reminder_delete" to "reminder_delete_ReminderID"
    # This case helps to provide unique callback for reminder distinguishing
    inline_callback.callback = inline_callback.callback + f"_{str(reminder_id)}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                inline_callback.to_inline_button()
            ]
        ]
    )
