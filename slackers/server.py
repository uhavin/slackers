import json
import logging

from typing import Union

from environs import Env
from fastapi import Depends, FastAPI
from starlette.status import HTTP_200_OK
from starlette.requests import Request
from starlette.responses import Response

from slackers.hooks import actions, commands, emit, events
from slackers.models import SlackAction, SlackChallenge, SlackCommand, SlackEnvelope
from slackers.verification import check_timeout, verify_signature

env = Env()
env.read_env()
log = logging.getLogger(__name__)

api = FastAPI()


@api.post(
    "/events",
    status_code=HTTP_200_OK,
    dependencies=[Depends(verify_signature), Depends(check_timeout)],
)
async def post_events(message: Union[SlackEnvelope, SlackChallenge]):
    if isinstance(message, SlackChallenge):
        return message.challenge

    emit(events, message.event["type"], payload=message)
    return Response()


@api.post(
    "/actions",
    status_code=HTTP_200_OK,
    dependencies=[Depends(verify_signature), Depends(check_timeout)],
)
async def post_actions(request: Request):
    form = await request.form()
    form_data = json.loads(form["payload"])

    # have the convenience of pydantic validation
    action = SlackAction(**form_data)

    emit(actions, action.type, payload=action)

    if action.actions:
        for triggered_action in action.actions:
            event_type = f"{action.type}:{triggered_action['action_id']}"
            emit(actions, event_type, action)
    if action.callback_id:
        event_type = f"{action.type}:{action.callback_id}"
        emit(actions, event_type, action)
    return Response()


@api.post(
    "/commands",
    status_code=HTTP_200_OK,
    dependencies=[Depends(verify_signature), Depends(check_timeout)],
)
async def post_commands(request: Request):
    form = await request.form()
    command = SlackCommand(**form)
    emit(commands, command.command.lstrip("/"), command)

    return Response()
