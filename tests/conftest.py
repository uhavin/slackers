import os
import time

import pytest
from fastapi import FastAPI

from starlette.testclient import TestClient

from slackers.server import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app=app)


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
    os.environ["SLACK_SIGNING_SECRET"] = "SLACK_SIGNING_SECRET"
