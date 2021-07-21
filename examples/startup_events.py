import asyncio
from async_event_bus import event_bus_task, define_handler, define_producer

async def handler_func(event):
    print(event)

event_bus = event_bus_task(
    handlers = [
        define_handler(
            filter=lambda event: True,
            handler=handler_func,
        )
    ],
    producers=[],
    startup_events=[
        "hello",
        "world"
    ]
)

asyncio.run(event_bus)