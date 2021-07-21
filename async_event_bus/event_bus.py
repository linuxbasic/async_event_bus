import queue
import asyncio
from typing import List, Optional
from async_event_bus.types import EventHandler, EventProducer, Event
from async_event_bus.utils import get_from_queue_or_stop
from async_event_bus.producer_task import producer_task
from async_event_bus.handler_task import handler_task

async def event_bus_task(handlers: List[EventHandler], producers: List[EventProducer], startup_events: Optional[List[Event]]=None, stop_event: Optional[asyncio.Event] = None, debug_queue: Optional[queue.Queue] = None):
    stop_event = stop_event or asyncio.Event()
    startup_events = startup_events or []
    bus_queue = asyncio.Queue()
    handler_queues = []

    for producer in producers:
        asyncio.create_task(producer_task(bus_queue, producer))

    for handler in handlers:
        handler_queue = asyncio.Queue()
        asyncio.create_task(handler_task(handler_queue, bus_queue, stop_event, handler))
        handler_queues.append(handler_queue)

    for event in startup_events:
        await bus_queue.put(event)

    while True:
        event = await get_from_queue_or_stop(bus_queue, stop_event)

        if event:
            for handler_queue in handler_queues:
                await handler_queue.put(event)
            if debug_queue:
                debug_queue.put(event)
            bus_queue.task_done()
            continue
        return


