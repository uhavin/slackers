# Slackers

Slackers is a FastAPI implementation to handle Slack interactions.  

This is still a work in progress.

# Example usage

```python
from slackers.hooks import actions, commands, events
from slackers.models import SlackAction, SlackEnvelope
from slackers.server import api

log = logging.getLogger(__name__)


@events.on("app_mention")
def handle_mention(payload: SlackEnvelope):
    log.info("App was mentioned.")
    log.debug(payload)


@actions.on("block_actions")
def handle_action(payload: SlackAction):
    log.info("Action started.")
    log.debug(payload)


@commands.on("foo")  # responds to "/foo"  
def handle_command(payload):
    log.info("Command received")
    log.debug(payload)


app = api
```
