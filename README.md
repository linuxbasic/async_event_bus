# Async Event Bus

The async event bus let small tasks exchange event messages asynchronously.

```python
import asyncio
from async_event_bus import event_bus_task, define_handler, define_producer

async def proucer_func():
    while True:
        asyncio.sleep(10)
        yield "hello"

async def handler_func(event):
    yield f"{event} world"

def event_filter(event):
    return event == "hello"

event_bus = event_bus_task(
    handlers = [
        define_handler(
            filter=event_filter,
            handler=handler_func,
        )
    ],
    producers=[
        define_producer(
            producer=proucer_func,
        )
    ]
)

asyncio.run(event_bus)
```

## Building Blocks

### Producer Function

Producer functions read external sources and publishes events on the event bus. The producer function gets invoked once when the bus starts and should `yield` events.

### Handler Function

Producer functions get called for each relevant event. Optionally they can publish new messages on the bus.

### Filter Function

Filter functions decide if a event gets handled by a handler function. The function should be synchronous and only use the content of the event to decide if it is relevant.

## Features

- **Shared Context**: Multiple producer and handler functions can optionally share common state by passing it as context. [Example](examples/shared_context.py)
- **Startup Events**: Dispatch a bunch of events after the bus has started. [Example](examples/startup_events.py)
- **Debug Utils**: You can run the event bus in an other tread and inspect the published messages. [Tests](tests/)