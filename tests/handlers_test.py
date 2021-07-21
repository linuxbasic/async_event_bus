from async_event_bus import define_handler
from async_event_bus.thread_runner import start_event_bus_thread
from async_event_bus.types import EventGenerator, Event
from async_event_bus.utils import get_messages
from queue import Queue

def test_async_yield_handle_event():
    debug_queue = Queue()

    async def handler_function(event: Event) -> EventGenerator:
        yield "test-2"
        yield "test-3"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[
            define_handler(filter_func=lambda event: event == "test-1", handler_func=handler_function),
        ],
        producers=[],
        debug_queue=debug_queue,
        startup_events=["test-1"]
    )

    expcted_messages = {"test-1", "test-2", "test-3"}
    received_messages = get_messages(debug_queue, 3)

    assert received_messages == expcted_messages
    stop_event_bus_thread()


def test_sync_yield_handle_event():
    debug_queue = Queue()

    def handler_function(event: Event) -> EventGenerator:
        yield "test-2"
        yield "test-3"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[
            define_handler(filter_func=lambda event: event == "test-1", handler_func=handler_function),
        ],
        producers=[],
        debug_queue=debug_queue,
        startup_events=["test-1"]
    )

    expcted_messages = {"test-1", "test-2", "test-3"}
    received_messages = get_messages(debug_queue, 3)

    assert received_messages == expcted_messages
    stop_event_bus_thread()


def test_async_return_handle_event():
    debug_queue = Queue()

    async def handler_function(event: Event) -> EventGenerator:
        return "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[define_handler(filter_func=lambda event: event == "test-1", handler_func=handler_function)],
        producers=[],
        debug_queue=debug_queue,
        startup_events=["test-1"]
    )

    expcted_messages = {"test-1", "test-2"}
    received_messages = get_messages(debug_queue, 2)

    assert received_messages == expcted_messages
    stop_event_bus_thread()


def test_sync_return_handle_event():
    debug_queue = Queue()

    def handler_function(event: Event) -> EventGenerator:
        return "test-2"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[define_handler(filter_func=lambda event: event == "test-1", handler_func=handler_function),],
        producers=[],
        debug_queue=debug_queue,
        startup_events=["test-1"]
    )

    expcted_messages = {"test-1", "test-2"}
    received_messages = get_messages(debug_queue, 2)

    assert received_messages == expcted_messages
    stop_event_bus_thread()

def test_filter_events():
    debug_queue = Queue()

    async def handler_function(event: Event) -> EventGenerator:
        yield "test-2"

    def filter_function(event: Event) -> bool:
        return event == "test-1"

    stop_event_bus_thread = start_event_bus_thread(
        handlers=[
            define_handler(filter_func=filter_function, handler_func=handler_function),
        ],
        producers=[],
        debug_queue=debug_queue,
        startup_events=["test-1"]
    )

    expcted_messages = {"test-1", "test-2"}
    received_messages = get_messages(debug_queue, 2)

    assert received_messages == expcted_messages
    stop_event_bus_thread()
