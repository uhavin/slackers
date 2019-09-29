from slackers.messaging.composition import MessageBuilder


def add_divider_should_put_divider_in_message_blocks():
    message = MessageBuilder()
    message.add_divider()
    assert message.dict() == {"channel": None, "blocks": [{"type": "divider"}]}


def creating_section_should_add_section():
    message = MessageBuilder()
    message.create_section(text="Hello World")

    expect = {
        "channel": None,
        "blocks": [
            {"type": "section", "text": {"text": "Hello World", "type": "mrkdwn"}}
        ],
    }

    assert message.dict() == expect


def create_section_should_return_the_section_to_allow_modification():
    message = MessageBuilder()
    section = message.create_section(text="Hello World")
    section.text.type = "plain_text"

    expect = {
        "channel": None,
        "blocks": [
            {"type": "section", "text": {"text": "Hello World", "type": "plain_text"}}
        ],
    }

    assert message.dict() == expect


def add_secction_with_button_should_add_section_with_accessory_button():
    message = MessageBuilder()
    message.create_section_with_button(
        text="Hello World", button_text="Push it", button_value="push_it"
    )
    expect = {
        "channel": None,
        "blocks": [
            {
                "type": "section",
                "text": {"text": "Hello World", "type": "mrkdwn"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Push it", "emoji": True},
                    "value": "push_it",
                },
            }
        ],
    }

    assert message.dict() == expect


def slack_blocks_should_return_blocks_as_jsonable_list():
    message = MessageBuilder()
    message.add_divider()
    message.add_divider()
    assert message.slack_blocks() == [{"type": "divider"}, {"type": "divider"}]
