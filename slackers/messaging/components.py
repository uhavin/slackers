from typing import List, Union
from pydantic import BaseModel, UrlStr


class PlainText(BaseModel):
    type: str = "plain_text"
    text: str
    emoji: bool = True


class Divider(BaseModel):
    type: str = "divider"


class Section(BaseModel):
    type: str = "section"
    text: PlainText


class Image(BaseModel):
    type: str = "image"
    image_url: UrlStr
    title: PlainText = None
    alt_text: str = ""


class Context(BaseModel):
    type: str = "context"
    elements: List[PlainText, Image]


class Option(BaseModel):
    value: str
    text: PlainText


class Select(BaseModel):
    placeholder: PlainText
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
    elements: List[
        Union[StaticSelect, UsersSelect, ChannelsSelect, ConversationsSelect]
    ]
