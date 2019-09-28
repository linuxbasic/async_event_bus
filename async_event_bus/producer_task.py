from async_event_bus.types import EventProducer
from async_event_bus.utils import forward_events

import asyncio

async def producer_task(outbox_queue: asyncio.Queue, producer: EventProducer):
    await forward_events(producer(), outbox_queue)