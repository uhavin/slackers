from pydantic import UrlStr
from typing_extensions import Literal

from .common import SlackModel


class Element(SlackModel):
    pass


class Text(Element):
    type: Literal["plain_text", "mrkdwn"] = "mrkdwn"
    text: str


class EmojiText(Text):
    emoji: bool = True


class InteractiveElement(Element):
    pass


class ButtonText(EmojiText):
    type: Literal["plain_text"] = "plain_text"


class Button(InteractiveElement):
    type: Literal["button"] = "button"
    text: ButtonText


class Image(Element):
    type: str = "image"
    image_url: UrlStr
    alt_text: str = ""


class TitleImage(Image):
    title: EmojiText = None
