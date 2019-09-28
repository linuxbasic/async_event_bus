from async_event_bus.types import EventHandler, FilterFunction, EventHandlerFunction, Context, EventGenerator, Event


def define_handler(filter: FilterFunction, handler: EventHandlerFunction, context: Context) -> EventHandler:
    def handle(event: Event) -> EventGenerator:
        if filter(event):
            return handler(event, context)
    return handle