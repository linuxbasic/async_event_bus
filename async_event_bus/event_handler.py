from async_event_bus.types import EventHandler, FilterFunction, EventHandlerFunction, Context, EventGenerator, Event
from typing import Optional
from async_event_bus.utils import wrap_func

def define_handler(filter_func: FilterFunction, handler_func: EventHandlerFunction, context: Optional[Context] = None) -> EventHandler:
    wrapped_func = wrap_func(handler_func)
    def handle(event: Event) -> EventGenerator:
        if filter_func(event):
            if context:
                return wrapped_func(event, context)
            return wrapped_func(event)
    return handle