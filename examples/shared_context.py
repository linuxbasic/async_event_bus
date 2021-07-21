import asyncio
from async_event_bus import event_bus_task, define_handler, define_producer

context_object = {
    "counter": 1
}

async def producer_func(context):
    while True:
        event = "hello " * context["counter"]
        print("produce", event)
        yield event
        await asyncio.sleep(1)

async def handler_func(event, context):
    print("handle", event)
    context["counter"] += 1

def event_filter(event):
    print("filter", event)
    return "hello" in event

event_bus = event_bus_task(
    handlers = [
        define_handler(
            filter=event_filter,
            handler=handler_func,
            context=context_object,
        )
    ],
    producers=[
        define_producer(
            producer=producer_func,
            context=context_object,
        )
    ]
)

asyncio.run(event_bus)