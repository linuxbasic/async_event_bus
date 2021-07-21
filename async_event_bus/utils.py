from typing import Optional, AsyncGenerator, Generator, Coroutine, Any, Set
from async_event_bus.types import EventGenerator, Event
import asyncio
from queue import Queue
import inspect
from functools import wraps

async def forward_events(from_generator: EventGenerator, to_queue: asyncio.Queue, ):
    if isinstance(from_generator, AsyncGenerator):
        async for event in from_generator:
            await to_queue.put(event)
    elif isinstance(from_generator, Generator):
        for event in from_generator:
                    await to_queue.put(event)
    elif isinstance(from_generator, Coroutine):
        event = await from_generator
        if event:
            await to_queue.put(event)
    elif from_generator is not None:
        await to_queue.put(from_generator)

async def run_func(queue: asyncio.Queue, func, *args, **kwargs):
    if inspect.isasyncgenfunction(func):
        async for event in func(*args, **kwargs):
            print("isasyncgenfunction",func,event)
            await queue.put(event)
    elif inspect.isgeneratorfunction(func):
        for event in func(*args, **kwargs):
            print("isgeneratorfunction",func, event)
            await queue.put(event)
    elif inspect.iscoroutinefunction(func):
        event = await func(*args, **kwargs)
        print("iscoroutinefunction",func, event)
        if event:
            await queue.put(event)
    elif inspect.isfunction(func):
        event = func(*args, **kwargs)
        print("isfunction", func, event)
        if event:
            await queue.put(event)
    else:
        print("else", func)


def wrap_func(func):
    if inspect.isasyncgenfunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async for event in func(*args, **kwargs):
                yield event
        return wrapper
    if inspect.isgeneratorfunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for event in func(*args, **kwargs):
                yield event
        return wrapper
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            yield await func(*args, **kwargs)
        return wrapper
    if inspect.isfunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            yield func(*args, **kwargs)
        return wrapper





async def get_from_queue_or_stop(queue: asyncio.Queue, stop_event: asyncio.Event) -> Optional[Event]:
    queue_get_task = asyncio.create_task(queue.get())
    stop_event_task = asyncio.create_task(stop_event.wait())
    done, _ = await asyncio.wait({queue_get_task, stop_event_task}, return_when=asyncio.FIRST_COMPLETED)

    if queue_get_task in done:
        stop_event_task.cancel()
        return queue_get_task.result()

    if stop_event_task in done:
        queue_get_task.cancel()
        return

def get_messages(queue: Queue, count: int, timeout: int = 1) -> Set[Any]:
    result = set()
    for _ in range(count):
        result.add(queue.get(timeout=timeout))

    return result