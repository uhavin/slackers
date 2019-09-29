from typing_extensions import Literal

from pydantic import BaseModel

from .elements import EmojiText


class Accessory(BaseModel):
    type: str
    value: str
    text: EmojiText


class ButtonText(EmojiText):
    type: Literal["plain_text"] = "plain_text"


class Button(Accessory):
    type: Literal["button"] = "button"
    text: ButtonText
