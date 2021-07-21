from async_event_bus.types import EventProducer
from async_event_bus.utils import run_func

import asyncio

async def producer_task(outbox_queue: asyncio.Queue, producer_func: EventProducer):
    await run_func(outbox_queue, producer_func)