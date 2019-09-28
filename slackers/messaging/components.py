from typing import List, Union

from pydantic import BaseModel, UrlStr

from .accessories import Accessory
from .common_elements import EmojiText, Text


class SlackBlock(BaseModel):
    type: str


class Divider(SlackBlock):
    type: str = "divider"


class Section(BaseModel):
    type: str = "section"
    text: EmojiText


class AccessorySection(Section):
    text: Text
    accessory: Accessory


class Image(BaseModel):
    type: str = "image"
    image_url: UrlStr
    title: EmojiText = None
    alt_text: str = ""


class Context(BaseModel):
    type: str = "context"
    elements: List[Union[EmojiText, Image]]


class Option(BaseModel):
    value: str
    text: EmojiText


class Select(BaseModel):
    placeholder: EmojiText
    action_id: str


class ChannelsSelect(Select):
    type: str = "channels_select"


class UsersSelect(Select):
    type: str = "users_select"


class ConversationsSelect(Select):
    type: str = "conversations_select"


class StaticSelect(Select):
    type: str = "static_select"
    options: List[Option]


class Actions(BaseModel):
    type: str = "actions"
    elements: List[Select]
