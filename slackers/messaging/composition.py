from pydantic import BaseModel
from typing import List, Union

from fastapi.encoders import jsonable_encoder

from .accessories import Button, ButtonText
from .elements import Text, Image
from .blocks import AccessorySection, Divider, Section, SlackBlock, Context, Actions


class ActionsBuilder(Actions):
    elements: List[Union[Button]] = list()
    pass


class ContextBuilder(Context):
    elements: List[Union[Text, Image]] = list()

    def add(self, element: Union[Text, Image]) -> None:
        self.elements.append(element)

    def add_text(self, text) -> None:
        text = Text(text=text)
        self.add(text)

    def add_image(self, href, alt) -> None:
        image = Image(image_url=href, alt_text=alt)
        self.elements.append(image)


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
    ) -> AccessorySection:
        button_text_obj = ButtonText(text=button_text)
        button = Button(text=button_text_obj, value=button_value)
        section = AccessorySection(text=Text(text=text), accessory=button)
        self.add(section)
        return section

    def create_context(self) -> ContextBuilder:
        context = ContextBuilder()
        self.add(context)
        return context
