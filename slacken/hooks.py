import asyncio
import logging

from pyee import BaseEventEmitter

events = BaseEventEmitter()
actions = BaseEventEmitter()
commands = BaseEventEmitter()


def emit(emitter, event, payload):
    logging.getLogger(__name__).debug(f"emitting event: {event}")
    logging.getLogger(__name__).debug(payload)

    async def _emit_async(emitter, event, payload):
        emitter.emit(event, payload)

    loop = asyncio.get_event_loop()
    loop.create_task(_emit_async(emitter, event, payload))
