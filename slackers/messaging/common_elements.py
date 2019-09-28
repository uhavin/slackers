from pydantic import BaseModel
from typing_extensions import Literal


class Text(BaseModel):
    type: Literal["plain_text", "mrkdwn"] = "mrkdwn"
    text: str


class EmojiText(Text):
    emoji: bool = True
