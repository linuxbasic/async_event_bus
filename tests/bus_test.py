from async_event_bus import start_event_bus_thread, define_handler, define_producer
from async_event_bus.types import Context, EventGenerator, Event
from queue import Queue
import pytest
import threading
from typing import Set, Any

def get_messages(queue: Queue, count: int) -> Set[Any]:
    result = set()
    for _ in range(count):
        result.add(queue.get(timeout=1))

    return result

def test_producer():
    debug_queue = Queue()
    context = object()

    async def producer_function(context: Context) -> EventGenerator:
        yield "test-1"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[define_producer(producer=producer_function, context=context)],
        debug_queue=debug_queue
    )

    assert debug_queue.get(timeout=1) == "test-1"
    stop_event_bus_thread()

def test_message_bus_stopped():
    debug_queue = Queue()
    context = object()

    async def producer_function(context: Context) -> EventGenerator:
        yield "test-1"

    stop_event_bus_thread = start_event_bus_thread(
        [],
        [define_producer(producer=producer_function, context=context)],
        debug_queue
    )

    assert threading.active_count() == 2
    stop_event_bus_thread()
    assert threading.active_count() == 1

def test_multiple_producers():
    debug_queue = Queue()
    context = object()

    async def producer_function_1(context: Context) -> EventGenerator:
        yield "test-1"

    async def producer_function_2(context: Context) -> EventGenerator:
        yield "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        [],
        [
            define_producer(producer=producer_function_1, context=context),
            define_producer(producer=producer_function_2, context=context),
        ],
        debug_queue
    )

    expcted_messages = {"test-1", "test-2"}
    received_messages = get_messages(debug_queue, 2)

    assert received_messages == expcted_messages
    stop_event_bus_thread()

def test_event_handler():
    debug_queue = Queue()
    context = object()

    async def producer_function(context: Context) -> EventGenerator:
        yield "test-1"
        yield "test-2"

    async def handler_function_1(event: Event, context: Context) -> EventGenerator:
        yield "test-3"

    async def handler_function_2(event: Event, context: Context) -> EventGenerator:
        yield "test-4"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[
            define_handler(filter=lambda event: event=="test-1", handler=handler_function_1, context=context),
            define_handler(filter=lambda event: event=="test-2", handler=handler_function_2, context=context),
        ],
        producers=[define_producer(producer=producer_function, context=context)],
        debug_queue=debug_queue
    )

    expcted_messages = {"test-1", "test-2", "test-3", "test-4"}
    received_messages = get_messages(debug_queue, 4)

    assert received_messages == expcted_messages
    stop_event_bus_thread()