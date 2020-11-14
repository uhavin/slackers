import json

import pytest
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from slackers.hooks import actions
from slackers.models import SlackAction
from slackers.registry import R


@pytest.fixture(autouse=True)
def reset_registry():
    R.callbacks = {}


@pytest.fixture
def action_defaults():
    action_defaults = SlackAction(type="...", token="...")
    return action_defaults.dict()


@pytest.fixture
def message_action(action_defaults):
    action_defaults.update(
        {
            "token": "TOKEN",
            "callback_id": "CALLBACK_ID",
            "trigger_id": "TRIGGER_ID",
            "response_url": "https://example.com/response",
            "type": "message_action",
            "user": {"id": "USER_ID", "name": "USER_NAME"},
            "message": {},
            "channel": {"id": "CHANNEL_ID", "name": "CHANNEL_NAME"},
            "team": {"id": "TEAM_ID", "domain": "TEAM_DOMAIN"},
            "actions": [],
            "view": {},
        }
    )
    return action_defaults


@pytest.fixture
def interactive_message(message_action):
    message_action.update(
        {
            "type": "interactive_message",
            "actions": [
                {"name": "ACTION_1_NAME", "type": "ACTION_1_TYPE"},
                {"name": "ACTION_2_NAME", "type": "ACTION_2_TYPE"},
            ],
        }
    )
    return message_action


@pytest.fixture
def block_actions(action_defaults):
    action_defaults.update(
        {
            "token": "TOKEN",
            "trigger_id": "TRIGGER_ID",
            "response_url": "https://example.com/response",
            "type": "block_actions",
            "user": {"id": "USER_ID", "name": "USER_NAME"},
            "message": {},
            "channel": {"id": "CHANNEL_ID", "name": "CHANNEL_NAME"},
            "team": {"id": "TEAM_ID", "domain": "TEAM_DOMAIN"},
            "actions": [{"action_id": "ACTION_ID_1"}, {"action_id": "ACTION_ID_2"}],
            "view": {},
        }
    )
    return action_defaults


@pytest.fixture
def view_submission(action_defaults):
    action_defaults.update(
        {
            "type": "view_submission",
            "team": {},
            "user": {},
            "view": {
                "id": "VIEW_ID",
                "type": "modal",
                "title": {},
                "submit": {},
                "blocks": [],
                "private_metadata": "private!",
                "callback_id": "VIEW_CALLBACK_ID",
                "state": {
                    "values": {
                        "multi-line": {
                            "ml-value": {
                                "type": "plain_text_input",
                                "value": "This is my example inputted value",
                            }
                        }
                    }
                },
                "hash": "156663117.cd33ad1f",
            },
        }
    )
    return action_defaults


@pytest.fixture
def view_closed(action_defaults):
    action_defaults.update(
        {
            "type": "view_closed",
            "team": {"id": "TXXXXXX", "domain": "coverbands"},
            "user": {"id": "UXXXXXX", "name": "dreamweaver"},
            "view": {"callback_id": "VIEW_CLOSED_CALLBACK_ID"},
            "api_app_id": "AXXXXXX",
            "is_cleared": False,
        }
    )
    return action_defaults


@pytest.mark.usefixtures("pass_header_verification")
def post_message_actions_should_emit_actions_event_with_payload(
    mocker, client: TestClient, test_headers, message_action
):
    action_payload = json.dumps(message_action)
    base_event_callee = mocker.Mock()

    @actions.on("message_action")
    def on_message_action(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=message_action)


@pytest.mark.usefixtures("pass_header_verification")
def post_message_actions_should_emit_callback_id_event_with_payload(
    mocker, client: TestClient, test_headers, message_action
):
    specific_event_callee = mocker.Mock()
    action_payload = json.dumps(message_action)

    @actions.on("message_action:CALLBACK_ID")
    def on_message_action_callback_id(payload):
        specific_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee.assert_called_once_with(payload=message_action)


@pytest.mark.usefixtures("pass_header_verification")
def post_block_actions_should_emit_actions_event_with_payload(
    mocker, client: TestClient, test_headers, block_actions
):
    action_payload = json.dumps(block_actions)
    base_event_callee = mocker.Mock()

    @actions.on("block_actions")
    def on_foo(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=block_actions)


@pytest.mark.usefixtures("pass_header_verification")
def post_block_actions_should_emit_action_event_with_payload(
    mocker, client: TestClient, test_headers, block_actions
):
    action_payload = json.dumps(block_actions)
    specific_event_callee_1 = mocker.Mock()
    specific_event_callee_2 = mocker.Mock()

    @actions.on("block_actions:ACTION_ID_1")
    def on_block_actions_action_id_1(payload):
        specific_event_callee_1(payload=payload)

    @actions.on("block_actions:ACTION_ID_2")
    def on_block_actions_action_id_2(payload):
        specific_event_callee_2(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee_1.assert_called_once_with(payload=block_actions)
    specific_event_callee_2.assert_called_once_with(payload=block_actions)


@pytest.mark.usefixtures("pass_header_verification")
def post_view_submission_should_emit_submission_event_with_payload(
    mocker, client: TestClient, test_headers, view_submission
):
    # test that callback_id is not required
    view_submission["view"].pop("callback_id")
    action_payload = json.dumps(view_submission)
    base_event_callee = mocker.Mock()

    @actions.on("view_submission")
    def on_view_submission_callback_id(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=view_submission)


@pytest.mark.usefixtures("pass_header_verification")
def post_view_submission_should_emit_selected_action_event_with_payload(
    mocker, client: TestClient, test_headers, view_submission
):
    action_payload = json.dumps(view_submission)
    specific_event_callee = mocker.Mock()

    @actions.on("view_submission:VIEW_CALLBACK_ID")
    def on_view_submission_callback_id(payload):
        specific_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee.assert_called_once_with(payload=view_submission)


@pytest.mark.usefixtures("pass_header_verification")
def post_block_actions_should_return_a_custom_response(
    client: TestClient, test_headers, block_actions
):
    action_payload = json.dumps(block_actions)
    from slackers.hooks import responder

    @responder("block_actions:ACTION_ID_1")
    def custom_response(actual_payload):
        from starlette.responses import JSONResponse

        assert actual_payload == block_actions
        return JSONResponse(content={"custom": "Custom Response"})

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    assert {"custom": "Custom Response"} == response.json()


@pytest.mark.usefixtures("pass_header_verification")
def post_interactive_message_should_emit_interactive_message_event_with_payload(
    mocker, client: TestClient, test_headers, interactive_message
):
    interactive_message_payload = json.dumps(interactive_message)
    base_event_callee = mocker.Mock()

    @actions.on("interactive_message")
    def on_foo(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions",
        data={"payload": interactive_message_payload},
        headers=test_headers,
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=interactive_message)


@pytest.mark.usefixtures("pass_header_verification")
def post_interactive_message_should_emit_interactive_message_event_names_with_payload(
    mocker, client: TestClient, test_headers, interactive_message
):
    interactive_message_payload = json.dumps(interactive_message)
    base_event_callee_1 = mocker.Mock()
    base_event_callee_2 = mocker.Mock()

    @actions.on("interactive_message:ACTION_1_NAME")
    def on_foo(payload):
        base_event_callee_1(payload=payload)

    @actions.on("interactive_message:ACTION_2_NAME")
    def on_foo(payload):
        base_event_callee_2(payload=payload)

    response = client.post(
        url="/actions",
        data={"payload": interactive_message_payload},
        headers=test_headers,
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee_1.assert_called_once_with(payload=interactive_message)
    base_event_callee_2.assert_called_once_with(payload=interactive_message)


@pytest.mark.usefixtures("pass_header_verification")
def post_interactive_message_should_emit_interactive_message_event_types_with_payload(
    mocker, client: TestClient, test_headers, interactive_message
):
    interactive_message_payload = json.dumps(interactive_message)
    base_event_callee_1 = mocker.Mock()
    base_event_callee_2 = mocker.Mock()

    @actions.on("interactive_message:ACTION_1_TYPE")
    def on_foo(payload):
        base_event_callee_1(payload=payload)

    @actions.on("interactive_message:ACTION_2_TYPE")
    def on_foo(payload):
        base_event_callee_2(payload=payload)

    response = client.post(
        url="/actions",
        data={"payload": interactive_message_payload},
        headers=test_headers,
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee_1.assert_called_once_with(payload=interactive_message)
    base_event_callee_2.assert_called_once_with(payload=interactive_message)


@pytest.mark.usefixtures("pass_header_verification")
def post_interactive_message_should_emit_interactive_message_event_name_type_combo_with_payload(
    mocker, client: TestClient, test_headers, interactive_message
):
    interactive_message_payload = json.dumps(interactive_message)
    base_event_callee_1 = mocker.Mock()
    base_event_callee_2 = mocker.Mock()

    @actions.on("interactive_message:ACTION_1_NAME:ACTION_1_TYPE")
    def on_foo(payload):
        base_event_callee_1(payload=payload)

    @actions.on("interactive_message:ACTION_2_NAME:ACTION_2_TYPE")
    def on_foo(payload):
        base_event_callee_2(payload=payload)

    response = client.post(
        url="/actions",
        data={"payload": interactive_message_payload},
        headers=test_headers,
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee_1.assert_called_once_with(payload=interactive_message)
    base_event_callee_2.assert_called_once_with(payload=interactive_message)


@pytest.mark.usefixtures("pass_header_verification")
def post_interactive_message_should_be_able_to_return_custom_response(
    client: TestClient, test_headers, interactive_message
):

    from slackers.hooks import responder

    interactive_message_payload = json.dumps(interactive_message)

    @responder("interactive_message")
    def custom_response(actual_payload):
        from starlette.responses import JSONResponse

        assert actual_payload == interactive_message
        return JSONResponse(content={"custom": "Custom Response"})

    response = client.post(
        url="/actions",
        data={"payload": interactive_message_payload},
        headers=test_headers,
    )

    assert HTTP_200_OK == response.status_code
    assert {"custom": "Custom Response"} == response.json()


@pytest.mark.usefixtures("pass_header_verification")
def post_view_submission_should_return_a_custom_response(
    client: TestClient, test_headers, view_submission
):
    action_payload = json.dumps(view_submission)
    from slackers.hooks import responder

    @responder("view_submission:VIEW_CALLBACK_ID")
    def custom_response(actual_payload):
        from starlette.responses import JSONResponse

        assert actual_payload == view_submission
        return JSONResponse(content={"custom": "Custom Response"})

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    assert {"custom": "Custom Response"} == response.json()


@pytest.mark.usefixtures("pass_header_verification")
def max_one_custom_response_should_be_possible(
    client: TestClient, test_headers, view_submission
):
    action_payload = json.dumps(view_submission)
    from slackers.hooks import responder

    @responder("view_submission")
    def custom_response(payload):
        ...  # pragma: no cover, exception raised before calling function

    @responder("view_submission:VIEW_CALLBACK_ID")
    def custom_response(payload):
        ...  # pragma: no cover, exception raised before calling function

    with pytest.raises(ValueError, match="Multiple response handlers found"):
        client.post(
            url="/actions", data={"payload": action_payload}, headers=test_headers
        )


@pytest.mark.usefixtures("pass_header_verification")
def handler_should_return_starlette_response(
    client: TestClient, test_headers, view_submission
):
    action_payload = json.dumps(view_submission)
    from slackers.hooks import responder

    @responder("view_submission:VIEW_CALLBACK_ID")
    def custom_response(payload):
        from requests import Response

        return Response()

    with pytest.raises(
        AssertionError, match="Please return a starlette.responses.Response"
    ):
        client.post(
            url="/actions", data={"payload": action_payload}, headers=test_headers
        )


@pytest.mark.usefixtures("pass_header_verification")
def post_view_closed_should_emit_closed_event(
    mocker, client: TestClient, test_headers, view_closed
):
    action_payload = json.dumps(view_closed)
    specific_event_callee = mocker.Mock()

    @actions.on("view_closed")
    def on_view_closed(payload):
        specific_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee.assert_called_once_with(payload=view_closed)


@pytest.mark.usefixtures("pass_header_verification")
def post_view_closed_should_emit_closed_event_callback_id(
    mocker, client: TestClient, test_headers, view_closed
):
    # This might be a nonexistent use case, but even so, if a callback id
    # is in a view_closed body, the callback_id event will be emitted as
    # a side effect anyway

    action_payload = json.dumps(view_closed)
    specific_event_callee = mocker.Mock()

    @actions.on("view_closed:VIEW_CLOSED_CALLBACK_ID")
    def on_view_closed_callback_id(payload):
        specific_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": action_payload}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee.assert_called_once_with(payload=view_closed)
