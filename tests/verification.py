import itertools

import pytest

from starlette.status import HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY
from starlette.testclient import TestClient

paths = ("/events", "/actions", "/commands")
incomplete_headers = (
    {},
    {"X-Slack-Request-Timestamp": "123"},
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
