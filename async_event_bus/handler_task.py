from typing import AsyncGenerator, Any
import asyncio
from async_event_bus.utils import get_from_queue_or_stop

async def handler_task(inbox_queue: asyncio.Queue, outbox_queue: asyncio.Queue, stop_event: asyncio.Event, handler_func: AsyncGenerator[Any, None]):
    while True:
        event = await get_from_queue_or_stop(inbox_queue, stop_event)
        if event:
            async for event in handler_func(event):
                await outbox_queue.put(event)
            continue
        return