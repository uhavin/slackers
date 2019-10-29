import hmac
import math
import os
import time
import logging

from hashlib import sha256

from fastapi import Header
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request
from starlette.exceptions import HTTPException


log = logging.getLogger(__name__)


async def verify_signature(
    request: Request,
    x_slack_signature: str = Header(...),
    x_slack_request_timestamp: str = Header(...),
):

    log.debug("Starting verification")

    body = await request.body()
    to_verify = str.encode("v0:" + str(x_slack_request_timestamp) + ":") + body
    our_hash = hmac.new(
        os.environ.get("SLACK_SIGNING_SECRET").encode(), to_verify, sha256
    ).hexdigest()
    our_signature = "v0=" + our_hash

    if not hmac.compare_digest(x_slack_signature, our_signature):
        log.info("Slack verification failed")
        raise HTTPException(HTTP_403_FORBIDDEN, "Forbidden")

    log.debug("Verification successful")


def check_timeout(x_slack_request_timestamp: str = Header(...)):
    timeout = 60 * 5  # 5 minutes
    request_timeout_time = int(x_slack_request_timestamp) + timeout
    current_time = math.ceil(time.time())

    if current_time > request_timeout_time:
        log.info("Slack request timestamp reached timeout")
        raise HTTPException(HTTP_403_FORBIDDEN, "Forbidden")
