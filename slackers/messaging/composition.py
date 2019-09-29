from typing import List

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from .accessories import Button, ButtonText
from .common_elements import Text, EmojiText
from .components import AccessorySection, Divider, Section, SlackBlock


class MessageBuilder(BaseModel):
    blocks: List[SlackBlock] = list()
    channel: str = None

    def slack_blocks(self):
        return jsonable_encoder(self.blocks)

    def add(self, block: SlackBlock):
        self.blocks.append(block)

    def add_divider(self):
        divider = Divider()
        self.add(divider)

    def create_section(self, text) -> Section:
        section = Section(text=Text(text=text))
        self.add(section)
        return section

    def create_section_with_button(
        self, text: str, button_text: str, button_value: str
    ):
        button_text_obj = ButtonText(text=button_text)
        button = Button(text=button_text_obj, value=button_value)
        section = AccessorySection(text=Text(text=text), accessory=button)
        self.add(section)
        return section
