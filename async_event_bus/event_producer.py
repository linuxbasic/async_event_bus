from async_event_bus.types import EventProducerFunction, EventProducer, Context, EventGenerator
from typing import Optional
from functools import wraps

def define_producer(producer_func: EventProducerFunction, context: Optional[Context] = None) -> EventProducer:
    
    def handle() -> EventGenerator:
        if context:
            return producer_func(context)
        return producer_func()
    return handle