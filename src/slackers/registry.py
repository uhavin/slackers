import typing

from starlette.responses import Response


class R:
    _registry = dict()

    @classmethod
    def add(cls, event, handler: typing.Callable[[dict], Response]):
        cls._registry[event] = handler

    @classmethod
    def handle(cls, event, payload):
        return cls._registry[event](payload)