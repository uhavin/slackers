# Slackers

Slack webhooks API served by FastAPI

## What is Slackers
Slackers is a [FastAPI](https://fastapi.tiangolo.com) implementation to handle Slack interactions and events.
It serves endpoints to receive [slash commands](https://api.slack.com/interactivity/slash-commands),
[app actions](https://api.slack.com/interactivity/actions), [interactive components](https://api.slack.com/interactivity/components). 
It also listens for events sent to the Slack Events API [Slack Events](https://api.slack.com/events-api). 

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
When an interaction is received, it will emit an event. You can listen
for these events as shown in the following examples.

On receiving a request, Slackers will emit an event which you can handle yourself.
Slackers will also respond to Slack with an (empty) http 200 response telling Slack
all is well received.

### Starting the server
As said, Slackers uses the excellent FastAPI to serve it's endpoints. Since you're here, 
I'm assuming you know what FastAPI is, but if you don't, you can learn all about 
how that works with [this tutorial](https://fastapi.tiangolo.com/tutorial/). 

Slackers offers you a router which you can include in your own FastAPI.
```python
from fastapi import FastAPI
from slackers.server import router

app = FastAPI()
app.include_router(router)

# Optionally you can use a prefix
app.include_router(router, prefix='/slack')
```

### Events
Once your server is running, the events endpoint is setup at `/events`, or if you use
the prefix as shown above, on `/slack/events`.

#### Accepting the challenge
When setting up Slack to [send events](https://api.slack.com/events-api#subscribing_to_event_types),
it will first send a challenge to verify your endpoint. Slackers detects when a challenge is sent.
You can simply start our api and Slackers will meet the challenge automatically.

#### Responding to events
On receiving an event, Slackers will emit a python event, which you can act upon as shown below.
```python
import logging
from slackers.hooks import events

log = logging.getLogger(__name__)

@events.on("app_mention")
def handle_mention(payload):
    log.info("App was mentioned.")
    log.debug(payload)
```


### Actions
Once your server is running, the actions endpoint is setup at `/actions`, or if you use
the prefix as shown above, on `/slack/actions`.

#### Responding to actions
On receiving an action, Slackers will emit a python event, which you can listen for as 
shown below. You can listen for the action type, or more specifically for the action id
or callback id linked to the action.
```python
import logging
from slackers.hooks import actions

log = logging.getLogger(__name__)

# Listening for the action type.
@actions.on("block_actions")
def handle_action(payload):
    log.info("Action started.")
    log.debug(payload)

# Listen for an action by it's action_id
@actions.on("block_actions:your_action_id")
def handle_action_by_id(payload):
    log.info("Action started.")
    log.debug(payload)

# Listen for an action by it's callback_id
@actions.on("block_actions:your_callback_id")
def handle_action_by_callback_id(payload):
    log.info(f"Action started.")
    log.debug(payload)
```

#### Custom responses
Slackers tries to be fast to respond to Slack. The events you are listening for with the
likes of `@actions.on(...)` are scheduled as an async task in a fire and forget fashion.
After scheduling these events, Slackers will by default return an empty 200 response which
might happen before the events are handled.

In some cases you might want to act on the payload and return a custom response to Slack.
For this, you can use the slackers `responder` decorator to define your custom handler
function. This function is then used as a callback instead of returning the default response.
You must ensure your custom handler returns a `starlette.responses.Response` or one of it's 
subclasses. You must furthermore ensure that there is only one responder responding to your
Slack request.

Please note that the events are also emitted, so you could have both `@actions.on("block_action:xyz")`
and `@responder("block_action:xyz")`. Just keep in mind that the event emissions are async and are
not awaited. In other words, Slackers doesn't ensure that the response (whether your custom response
or the default) is returned before or after the events are emitted.

```python
from starlette.responses import JSONResponse
from slackers.hooks import responder

@responder("block_actions:your_callback_id")
def custom_handler(payload):
    # handle your payload
    ...
    return JSONResponse(content={"custom": "Custom Response"})
```

### Slash commands
Once your server is running, the commands endpoint is setup at `/commands`, or if you use
the prefix as shown above, on `/slack/commands`. Slackers will emit an event with the name
of the command, so if your command is `/engage`, you can listen for the event `engage`
(without the slash)

#### Responding to slash commands
On receiving a command, Slackers will emit a python event, which you can listen for as shown below.
```python
import logging
from slackers.hooks import commands

log = logging.getLogger(__name__)


@commands.on("engage")  # responds to "/engage"  
def handle_command(payload):
    log.info("Command received")
    log.debug(payload)
```

### Async
Since events are emitted using pyee's Async event emitter, it is possible to define your event handlers
as async functions. Just keep in mind that errors are in this case emitted on the 'error' event. 

```python
import logging
from slackers.hooks import commands

log = logging.getLogger(__name__)

@commands.on('error')
def log_error(exc):
    log.error(str(exc))


@commands.on("engage")  # responds to "/engage"  
async def handle_command(payload):
    ...
```
