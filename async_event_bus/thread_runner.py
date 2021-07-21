from async_event_bus import event_bus_task
import threading
import asyncio
import queue
from typing import List, Optional, Coroutine, Callable
from async_event_bus.types import EventHandler, EventProducer, Event

def start_event_bus_thread(handlers: List[EventHandler], producers: List[EventProducer], startup_events: Optional[List[Event]]=None, debug_queue: Optional[queue.Queue] = None):
    loop = asyncio.new_event_loop()
    stop_event = asyncio.Event(loop=loop)
    
    def start_loop():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(event_bus_task(handlers, producers, startup_events, stop_event, debug_queue))

    def stop_event_bus_thread(timeout: Optional[int]=None):
        def set_stop_event():
           stop_event.set()
        loop.call_soon_threadsafe(set_stop_event)
        thread.join(timeout)

    thread = threading.Thread(target=start_loop)
    thread.start()
    return stop_event_bus_thread