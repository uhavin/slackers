import os
import time
import itertools

import pytest

from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from starlette.testclient import TestClient

paths = ("/events", "/actions", "/commands")
incomplete_headers = (
    {},
    {"X-Slack-Request-Timestamp": str(round(time.time()))},
    {"X-Slack-Signature": "FAKE_SIG"},
)


@pytest.mark.parametrize("path", paths)
def post_commands_should_verify_headers(path: str, client: TestClient):
    complete_but_invalid_headers = {
        "X-Slack-Request-Timestamp": "0",
        "X-Slack-Signature": "INVALID_SIGNATURE",
    }
    response = client.post(url=path, data={}, headers=complete_but_invalid_headers)
    assert HTTP_403_FORBIDDEN == response.status_code


@pytest.mark.parametrize("path,headers", itertools.product(paths, incomplete_headers))
def post_commands_should_require_headers(path: str, headers: dict, client: TestClient):
    response = client.post(url=path, data={}, headers=headers)
    assert HTTP_422_UNPROCESSABLE_ENTITY == response.status_code


def headers_should_be_verified(client: TestClient, mocker):
    timestamp_jan_1_2019_noon = 1546340400
    time = mocker.patch("slackers.verification.time")
    time.time.return_value = timestamp_jan_1_2019_noon + (5 * 60) - 1
    os.environ["SLACK_SIGNING_SECRET"] = "TEST_SECRET"
    signature = "v0=66c758f7c180af608f5984e07c562ad8033c2ccce8b21771655fa7dd8d480ebe"
    valid_headers = {
        "X-Slack-Request-Timestamp": str(timestamp_jan_1_2019_noon),
        "X-Slack-Signature": signature,
    }
    challenge = {
        "token": "SLACK_TOKEN",
        "challenge": "A REAL CHALLENGE",
        "type": "url_verification",
    }
    response = client.post("/events", json=challenge, headers=valid_headers)
    assert HTTP_200_OK == response.status_code


def timestamp_should_not_exceed_timeout(client: TestClient, mocker):
    timestamp_jan_1_2019_noon = 1546340400
    time = mocker.patch("slackers.verification.time")
    time.time.return_value = timestamp_jan_1_2019_noon + (5 * 60) + 1
    os.environ["SLACK_SIGNING_SECRET"] = "TEST_SECRET"
    signature = "v0=66c758f7c180af608f5984e07c562ad8033c2ccce8b21771655fa7dd8d480ebe"
    valid_headers = {
        "X-Slack-Request-Timestamp": str(timestamp_jan_1_2019_noon),
        "X-Slack-Signature": signature,
    }
    challenge = {
        "token": "SLACK_TOKEN",
        "challenge": "A REAL CHALLENGE",
        "type": "url_verification",
    }
    response = client.post("/events", json=challenge, headers=valid_headers)
    assert HTTP_403_FORBIDDEN == response.status_code
