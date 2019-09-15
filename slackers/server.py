import json
import logging

from typing import Union

from environs import Env
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_200_OK
from starlette.requests import Request
from starlette.responses import Response

from slackers.hooks import actions, commands, emit, events
from slackers.models import SlackAction, SlackChallenge, SlackEnvelope
from slackers.verification import verify_signature

env = Env()
env.read_env()
log = logging.getLogger(__name__)

api = FastAPI()


@api.post("/events", dependencies=[Depends(verify_signature)])
async def post_events(message: Union[SlackEnvelope, SlackChallenge]):
    if isinstance(message, SlackChallenge):
        return message.challenge

    emit(events, message.event["type"], payload=jsonable_encoder(message))
    return Response()


@api.post("/actions", status_code=HTTP_200_OK, dependencies=[Depends(verify_signature)])
async def post_actions(request: Request):
    form = await request.form()
    payload = json.loads(form["payload"])

    # have the convenience of pydantic validation
    action = SlackAction(**payload)

    emit(actions, action.type, payload=jsonable_encoder(action))

    return Response()


@api.post(
    "/commands", status_code=HTTP_200_OK, dependencies=[Depends(verify_signature)]
)
async def post_commands(request: Request):
    form = await request.form()
    command = form["command"]
    emit(commands, command.lstrip("/"), jsonable_encoder(form))

    return Response()
