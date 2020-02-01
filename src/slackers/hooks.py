import asyncio
import logging

from pyee import AsyncIOEventEmitter
from fastapi.encoders import jsonable_encoder

from .registry import R


def responder(event):
    def wrapper(original):
        R.add(event, original)
        return original

    return wrapper


class NamedEventEmitter(AsyncIOEventEmitter):
    def __init__(self, name, *args, **kwargs):
        self.name = name

        AsyncIOEventEmitter.__init__(self, *args, **kwargs)


events = NamedEventEmitter(name="events")
actions = NamedEventEmitter(name="actions")
commands = NamedEventEmitter(name="commands")


def emit(emitter: NamedEventEmitter, event, payload):
    async def _emit_async():
        emitter.emit(event, jsonable_payload)

    jsonable_payload = jsonable_encoder(payload)
    log = logging.getLogger(__name__)
    log.info(f"Emitting '{event}' using emitter '{emitter.name}'")
    log.debug(jsonable_payload)

    loop = asyncio.get_event_loop()
    loop.create_task(_emit_async())
