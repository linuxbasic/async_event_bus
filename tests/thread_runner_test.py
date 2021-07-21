from async_event_bus import define_producer
from async_event_bus.thread_runner import start_event_bus_thread
from async_event_bus.types import Context, EventGenerator
from queue import Queue
import threading

def test_thread_stopped():
    debug_queue = Queue()

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[],
        debug_queue=debug_queue
    )

    assert threading.active_count() == 2
    stop_event_bus_thread()
    assert threading.active_count() == 1