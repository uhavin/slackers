import pytest

from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from slackers.hooks import events


@pytest.mark.usefixtures("pass_header_verification")
def post_events_should_accept_slack_challenge(mocker, client: TestClient):
    @events.on("foo")
    def on_challenge(payload):
        inspection(payload=payload)

    inspection = mocker.Mock()
    slack_challenge = {
        "token": "TOKEN",
        "challenge": "CHALLENGE ACCEPTED",
        "type": "challenge",
    }
    headers = {"X-Slack-Request-Timestamp": "123", "X-Slack-Signature": "FAKE_SIG"}
    response = client.post(url="/events", json=slack_challenge, headers=headers)

    assert 200 == response.status_code
    assert '"CHALLENGE ACCEPTED"' == response.text
    assert inspection.called is False


@pytest.mark.usefixtures("pass_header_verification")
def post_events_should_emit_events_event_with_payload(mocker, client: TestClient):
    slack_envelope = {
        "token": "TOKEN",
        "team_id": "TEAM_ID",
        "api_app_id": "API_APP_ID",
        "event": {"type": "foo"},
        "type": "TYPE",
        "authed_users": [],
        "event_id": "EVENT_ID",
        "event_time": 1,
    }

    @events.on("foo")
    def on_foo(payload):
        inspection(payload=payload)

    inspection = mocker.Mock()
    headers = {"X-Slack-Request-Timestamp": "123", "X-Slack-Signature": "FAKE_SIG"}

    response = client.post(url="/events", json=slack_envelope, headers=headers)

    assert HTTP_200_OK == response.status_code
    inspection.assert_called_once_with(payload=slack_envelope)
