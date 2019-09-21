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
    elements: List[Union[PlainText, Image]]


class ChannelsSelect(BaseModel):
    type: str = "channels_select"
    placeholder: PlainText


class Actions(BaseModel):
    type: str = "actions"
    elements: List[Union[ChannelsSelect]]
