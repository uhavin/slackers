import os

import pytest

from starlette.testclient import TestClient

from slacken.server import api


@pytest.fixture
def client():
    return TestClient(app=api)


@pytest.fixture
def pass_header_verification(mocker):
    hmac = mocker.patch("slacken.verification.hmac")
    hmac.compare_digest.return_value = True


@pytest.fixture(autouse=True, scope="session")
def test_config():
    os.environ["SLACK_APP_ID"] = "SLACK_APP_ID"
    os.environ["SLACK_BOT_TOKEN"] = "SLACK_BOT_TOKEN"
    os.environ["SLACK_SIGNING_SECRET"] = "SLACK_SIGNING_SECRET"
