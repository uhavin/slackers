import json

import pytest

from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from slackers.hooks import actions


@pytest.mark.usefixtures("pass_header_verification")
def post_actions_should_emit_actions_event_with_payload(mocker, client: TestClient):
    slack_action_payload = {
        "token": "TOKEN",
        "callback_id": "CALLBACK_ID",
        "trigger_id": "TRIGGER_ID",
        "response_url": "https://example.com/response",
        "type": "foo",
        "user": {"id": "USER_ID", "name": "USER_NAME"},
        "message": {},
        "channel": {"id": "CHANNEL_ID", "name": "CHANNEL_NAME"},
        "team": {"id": "TEAM_ID", "domain": "TEAM_DOMAIN"},
    }

    slack_action = json.dumps(slack_action_payload)

    @actions.on("foo")
    def on_foo(payload):
        inspection(payload=payload)

    inspection = mocker.Mock()
    headers = {"X-Slack-Request-Timestamp": "123", "X-Slack-Signature": "FAKE_SIG"}

    response = client.post(
        url="/actions", data={"payload": slack_action}, headers=headers
    )

    assert HTTP_200_OK == response.status_code
    inspection.assert_called_once_with(payload=slack_action_payload)
