from async_event_bus.types import EventHandler
from async_event_bus.utils import forward_events
import asyncio
from async_event_bus.utils import get_from_queue_or_stop

async def handler_task(inbox_queue: asyncio.Queue, outbox_queue: asyncio.Queue, stop_event: asyncio.Event, handler: EventHandler):
    while True:
        event = await get_from_queue_or_stop(inbox_queue, stop_event)
        if event:
            result = handler(event)
            if result:
                await forward_events(result, outbox_queue)
            continue
        return