from typing import List

from pydantic import BaseModel

from .components import AccessorySection, Divider, Section, SlackBlock
from .accessories import Accessory, Button, ButtonText
from .common_elements import Text, EmojiText


class MessageBuilder(BaseModel):
    blocks: List[SlackBlock] = list()

    def add(self, block: SlackBlock):
        self.blocks.append(block)

    def add_divider(self):
        self.add(Divider())

    def create_section(self, text) -> Section:
        section = Section(text=EmojiText(text=text))
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
