from typing import List, Union

from .common import SlackModel
from .accessories import Accessory
from .elements import EmojiText, Text, Image


class SlackBlock(SlackModel):
    type: str


class Divider(SlackBlock):
    type: str = "divider"


class Section(SlackBlock):
    type: str = "section"
    text: Text


class AccessorySection(Section):
    text: Text
    accessory: Accessory


class Context(SlackBlock):
    type: str = "context"
    elements: List[Union[Text, Image]]


class Option(SlackModel):
    value: str
    text: EmojiText


class Select(SlackModel):
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


class Actions(SlackBlock):
    type: str = "actions"
    elements: List[Select]
