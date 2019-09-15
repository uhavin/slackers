import pytest

from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from slackers.hooks import commands


@pytest.mark.usefixtures("pass_header_verification")
def post_commands_should_emit_commands_event_with_payload(mocker, client: TestClient):
    @commands.on("foo")
    def on_foo(payload):
        inspection(payload=payload)

    inspection = mocker.Mock()
    headers = {"X-Slack-Request-Timestamp": "123", "X-Slack-Signature": "FAKE_SIG"}

    response = client.post(url="/commands", data={"command": "/foo"}, headers=headers)

    assert HTTP_200_OK == response.status_code
    inspection.assert_called_once_with(payload={"command": "/foo"})
