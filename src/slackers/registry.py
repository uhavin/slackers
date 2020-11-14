import typing

from starlette.responses import Response


class R:
    callbacks = dict()

    @classmethod
    def add(cls, event, handler: typing.Callable[[dict], Response]):
        cls.callbacks[event] = handler

    @classmethod
    def handle(cls, event: str, payload: dict):
        return cls.callbacks[event](payload)
