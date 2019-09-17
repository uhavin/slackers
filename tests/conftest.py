import os
import time

import pytest

from starlette.testclient import TestClient

from slackers.server import api


@pytest.fixture
def client():
    return TestClient(app=api)


@pytest.fixture
def test_headers():
    recent_timestamp = str(round(time.time()))
    return {
        "X-Slack-Request-Timestamp": recent_timestamp,
        "X-Slack-Signature": "FAKE_SIG",
    }


@pytest.fixture
def pass_header_verification(mocker):
    hmac = mocker.patch("slackers.verification.hmac")
    hmac.compare_digest.return_value = True


@pytest.fixture(autouse=True, scope="session")
def test_config():
    os.environ["SLACK_APP_ID"] = "SLACK_APP_ID"
    os.environ["SLACK_BOT_TOKEN"] = "SLACK_BOT_TOKEN"
    os.environ["SLACK_SIGNING_SECRET"] = "SLACK_SIGNING_SECRET"
