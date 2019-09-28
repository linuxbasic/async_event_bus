from async_event_bus.types import EventProducerFunction, EventProducer, Context, EventGenerator

def define_producer(producer: EventProducerFunction, context: Context) -> EventProducer:
    def handle() -> EventGenerator:
        return producer(context)
    return handle