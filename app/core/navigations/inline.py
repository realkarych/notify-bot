from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton


@dataclass(frozen=True)
class InlineCallback:
    """Represents inline callback object"""

    text: str
    callback: str

    def to_inline_button(self) -> InlineKeyboardButton:
        """Map Inline callback object to Aiogram inline button"""

        return InlineKeyboardButton(text=self.text, callback_data=self.callback)


cancel = InlineCallback(text="Отмена", callback="cancel")

hours = [InlineCallback(text=str(hour), callback=f"hour_{hour}") for hour in range(24)]
minutes = [InlineCallback(text=str(minute), callback=f"minute_{minute}") for minute in range(0, 60, 5)]
