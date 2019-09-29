from pydantic import BaseModel


class SlackModel(BaseModel):
    type: str
