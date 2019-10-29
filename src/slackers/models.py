from typing import List

from pydantic import BaseModel


class SlackBase(BaseModel):
    token: str


class SlackChallenge(SlackBase):
    challenge: str
    type: str


class SlackEnvelope(SlackBase):
    team_id: str
    api_app_id: str
    event: dict
    type: str
    authed_users: List[str]
    event_id: str
    event_time: int


class SlackAction(SlackBase):
    callback_id: str = None
    trigger_id: str = None
    response_url: str = None
    type: str = None
    user: dict = None
    message: dict = None
    channel: dict = None
    team: dict = None
    actions: list = None


class SlackCommand(SlackBase):
    user_id: str
    command: str
    response_url: str
    trigger_id: str
    user_id: str
    user_name: str
    team_id: str
    channel_id: str
