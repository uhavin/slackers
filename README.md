# Slackers

Slackers is a FastAPI implementation to handle Slack interactions.  
## Installation
You can install Slackers with pip
`$ pip install slackers`

## Configuration
### `SLACK_SIGNING_SECRET`
You must configure the slack signing secret. This will be used to 
verify the incoming requests signature.   
`$ export SLACK_SIGNING_SECRET=your_slack_signing_secret`

## Example usage
Slackers will listen for activity from the Events API on `/events`, for
interactive components on `/actions` and for slash commands on `/commands`.
When an interaction is received, it will send an event. You can listen
for these events as shown in the following examples.

```python
import logging

from slackers.hooks import actions, commands, events
from slackers.server import api

log = logging.getLogger(__name__)

@events.on("app_mention")
def handle_mention(payload):
    log.info("App was mentioned.")
    log.debug(payload)


@actions.on("block_actions")
def handle_action(payload):
    log.info("Action started.")
    log.debug(payload)

@actions.on("block_actions:action_id")
def handle_action_by_id(payload):
    log.info("Action started.")
    log.debug(payload)


@actions.on("block_actions:callback_id")
def handle_action_by_callback_id(payload):
    log.info(f"Action started.")
    log.debug(payload)


@commands.on("foo")  # responds to "/foo"  
def handle_command(payload):
    log.info("Command received")
    log.debug(payload)


app = api
```

Or, if you already have an API running, you can add slackers as a router
```python
from fastapi import FastAPI
from slackers.server import router as slack_router

...

my_app = FastAPI()
my_app.include_router(slack_router, prefix="/slack")
```
