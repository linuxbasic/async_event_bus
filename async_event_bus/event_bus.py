import queue
import asyncio
import threading
from typing import List, Optional
from async_event_bus.types import EventHandler, EventProducer
from async_event_bus.utils import get_from_queue_or_stop
from async_event_bus.producer_task import producer_task
from async_event_bus.handler_task import handler_task

async def event_bus_task(handlers: List[EventHandler], producers: List[EventProducer], stop_event: asyncio.Event, debug_queue: Optional[queue.Queue] = None):
    bus_queue = asyncio.Queue()
    handler_queues = []

    for producer in producers:
        asyncio.create_task(producer_task(bus_queue, producer))

    for handler in handlers:
        handler_queue = asyncio.Queue()
        asyncio.create_task(handler_task(handler_queue, bus_queue, stop_event, handler))
        handler_queues.append(handler_queue)

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


def start_event_bus_thread(handlers: List[EventHandler], producers: List[EventProducer], debug_queue: Optional[queue.Queue] = None):
    loop = asyncio.new_event_loop()
    stop_event = asyncio.Event(loop=loop)
    
    def start_loop():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(event_bus_task(handlers, producers, stop_event, debug_queue))

    def stop_event_bus_thread(timeout: Optional[int]=None):
        def set_stop_event():
           stop_event.set()
        loop.call_soon_threadsafe(set_stop_event)
        thread.join(timeout)

    thread = threading.Thread(target=start_loop)
    thread.start()
    return stop_event_bus_thread

