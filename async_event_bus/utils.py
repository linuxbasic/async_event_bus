from typing import Optional
from async_event_bus.types import EventGenerator, Event
import asyncio

async def forward_events(from_generator: EventGenerator, to_queue: asyncio.Queue, ):
    async for event in from_generator:
        await to_queue.put(event)

async def get_from_queue_or_stop(queue: asyncio.Queue, stop_event: asyncio.Event) -> Optional[Event]:
    queue_get_task = asyncio.create_task(queue.get())
    stop_event_task = asyncio.create_task(stop_event.wait())
    done, _ = await asyncio.wait({queue_get_task, stop_event_task}, return_when=asyncio.FIRST_COMPLETED)

    if queue_get_task in done:
        stop_event_task.cancel()
        return queue_get_task.result()

    if stop_event_task in done:
        queue_get_task.cancel()
        return