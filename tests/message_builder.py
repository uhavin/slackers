from slackers.messaging.composition import MessageBuilder, ContextBuilder


def channel_should_be_settable():
    message = MessageBuilder(channel="CHANNEL")
    message.add_divider()
    assert message.dict() == {"channel": "CHANNEL", "blocks": [{"type": "divider"}]}


def slack_blocks_should_return_blocks_as_jsonable_list():
    message = MessageBuilder()
    message.add_divider()
    message.add_divider()
    assert message.slack_blocks() == [{"type": "divider"}, {"type": "divider"}]


def add_divider_should_put_divider_in_message_blocks():
    message = MessageBuilder()
    message.add_divider()
    assert message.dict() == {"channel": None, "blocks": [{"type": "divider"}]}


def create_context_should_add_context_block():
    message = MessageBuilder()
    context = message.create_context()
    context.add_text(text="Hello World!")
    context.add_image(href="https://example.com/some.img", alt="Example")

    expect_blocks = [
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "Hello World!"},
                {
                    "type": "image",
                    "image_url": "https://example.com/some.img",
                    "alt_text": "Example",
                },
            ],
        }
    ]

    assert message.slack_blocks() == expect_blocks


def adding_built_context_should_add_context_block():
    context = ContextBuilder()
    context.add_text(text="Hello World!")
    context.add_image(href="https://example.com/some.img", alt="Example")

    message = MessageBuilder()
    message.add(context)

    expect_blocks = [
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "Hello World!"},
                {
                    "type": "image",
                    "image_url": "https://example.com/some.img",
                    "alt_text": "Example",
                },
            ],
        }
    ]

    assert message.slack_blocks() == expect_blocks


def creating_section_should_add_section():
    message = MessageBuilder()
    message.create_section(text="Hello World")

    expect_blocks = [
        {"type": "section", "text": {"text": "Hello World", "type": "mrkdwn"}}
    ]

    assert message.slack_blocks() == expect_blocks


def create_section_should_return_the_section_to_allow_modification():
    message = MessageBuilder()
    section = message.create_section(text="Hello World")
    section.text.type = "plain_text"

    expect_blocks = [
        {"type": "section", "text": {"text": "Hello World", "type": "plain_text"}}
    ]

    assert message.slack_blocks() == expect_blocks


def add_section_with_button_should_add_section_with_accessory_button():
    message = MessageBuilder()
    message.create_section_with_button(
        text="Hello World", button_text="Push it", button_value="push_it"
    )
    expect_blocks = [
        {
            "type": "section",
            "text": {"text": "Hello World", "type": "mrkdwn"},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Push it", "emoji": True},
                "value": "push_it",
            },
        }
    ]

    assert message.slack_blocks() == expect_blocks
