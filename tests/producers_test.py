from async_event_bus import define_producer
from async_event_bus.thread_runner import start_event_bus_thread
from async_event_bus.types import Context, EventGenerator
from async_event_bus.utils import get_messages
from queue import Queue

def test_async_yield_producer():
    debug_queue = Queue()
    context = object()

    async def producer_function(context: Context) -> EventGenerator:
        yield "test-1"
        yield "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[define_producer(producer_func=producer_function, context=context)],
        debug_queue=debug_queue
    )

    assert get_messages(debug_queue, 2) == {"test-1", "test-2"}

    stop_event_bus_thread()

def test_async_return_producer():
    debug_queue = Queue()
    context = object()

    async def producer_function(context: Context) -> EventGenerator:
        return "test-1"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[define_producer(producer_func=producer_function, context=context)],
        debug_queue=debug_queue
    )

    assert get_messages(debug_queue, 1) == {"test-1"}

    stop_event_bus_thread()

def test_sync_yield_producer():
    debug_queue = Queue()
    context = object()

    def producer_function(context: Context) -> EventGenerator:
        yield "test-1"
        yield "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[define_producer(producer_func=producer_function, context=context)],
        debug_queue=debug_queue
    )

    assert get_messages(debug_queue, 2) == {"test-1", "test-2"}

    stop_event_bus_thread()

def test_sync_return_producer():
    debug_queue = Queue()
    context = object()

    def producer_function(context: Context) -> EventGenerator:
        return "test-1"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[define_producer(producer_func=producer_function, context=context)],
        debug_queue=debug_queue
    )

    assert get_messages(debug_queue, 1) == {"test-1"}

    stop_event_bus_thread()

def test_multiple_producers():
    debug_queue = Queue()
    context = object()

    async def producer_function_1(context: Context) -> EventGenerator:
        yield "test-1"

    async def producer_function_2(context: Context) -> EventGenerator:
        yield "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[],
        producers=[
            define_producer(producer_func=producer_function_1, context=context),
            define_producer(producer_func=producer_function_2, context=context),
        ],
        debug_queue=debug_queue
    )

    expcted_messages = {"test-1", "test-2"}
    received_messages = get_messages(debug_queue, 2)

    assert received_messages == expcted_messages
    stop_event_bus_thread()