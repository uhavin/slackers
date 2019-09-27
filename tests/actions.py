import json

import pytest

from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from slackers.hooks import actions


@pytest.fixture
def message_action():
    return {
        "token": "TOKEN",
        "callback_id": "CALLBACK_ID",
        "trigger_id": "TRIGGER_ID",
        "response_url": "https://example.com/response",
        "type": "foo",
        "user": {"id": "USER_ID", "name": "USER_NAME"},
        "message": {},
        "channel": {"id": "CHANNEL_ID", "name": "CHANNEL_NAME"},
        "team": {"id": "TEAM_ID", "domain": "TEAM_DOMAIN"},
        "actions": [],
    }


@pytest.fixture
def block_action():
    return {
        "token": "TOKEN",
        "callback_id": None,
        "trigger_id": "TRIGGER_ID",
        "response_url": "https://example.com/response",
        "type": "foo",
        "user": {"id": "USER_ID", "name": "USER_NAME"},
        "message": {},
        "channel": {"id": "CHANNEL_ID", "name": "CHANNEL_NAME"},
        "team": {"id": "TEAM_ID", "domain": "TEAM_DOMAIN"},
        "actions": [{"action_id": "ACTION_ID_1"}, {"action_id": "ACTION_ID_2"}],
    }


@pytest.mark.usefixtures("pass_header_verification")
def post_message_actions_should_emit_actions_event_with_payload(
    mocker, client: TestClient, test_headers, message_action
):
    slack_action = json.dumps(message_action)
    base_event_callee = mocker.Mock()

    @actions.on("foo")
    def on_foo(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": slack_action}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=message_action)


@pytest.mark.usefixtures("pass_header_verification")
def post_message_actions_should_emit_callback_id_event_with_payload(
    mocker, client: TestClient, test_headers, message_action
):
    specific_event_callee = mocker.Mock()
    slack_action = json.dumps(message_action)

    @actions.on("foo:CALLBACK_ID")
    def on_foo_CALLBACK_ID(payload):
        specific_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": slack_action}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee.assert_called_once_with(payload=message_action)


@pytest.mark.usefixtures("pass_header_verification")
def post_block_actions_should_emit_actions_event_with_payload(
    mocker, client: TestClient, test_headers, block_action
):
    slack_action = json.dumps(block_action)
    base_event_callee = mocker.Mock()

    @actions.on("foo")
    def on_foo(payload):
        base_event_callee(payload=payload)

    response = client.post(
        url="/actions", data={"payload": slack_action}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    base_event_callee.assert_called_once_with(payload=block_action)


@pytest.mark.usefixtures("pass_header_verification")
def post_block_actions_should_emit_selected_action_event_with_payload(
    mocker, client: TestClient, test_headers, block_action
):
    slack_action = json.dumps(block_action)
    specific_event_callee_1 = mocker.Mock()
    specific_event_callee_2 = mocker.Mock()

    @actions.on("foo:ACTION_ID_1")
    def on_foo(payload):
        specific_event_callee_1(payload=payload)

    @actions.on("foo:ACTION_ID_2")
    def on_foo(payload):
        specific_event_callee_2(payload=payload)

    response = client.post(
        url="/actions", data={"payload": slack_action}, headers=test_headers
    )

    assert HTTP_200_OK == response.status_code
    specific_event_callee_1.assert_called_once_with(payload=block_action)
    specific_event_callee_2.assert_called_once_with(payload=block_action)
