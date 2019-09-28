from typing import Callable, Generator, List, AsyncGenerator, Any, Optional

Event = Any
Context = Any
EventGenerator = AsyncGenerator[Event, None]
FilterFunction = Callable[[Event], bool]
EventHandlerFunction = Callable[[Event, Context], EventGenerator]
EventProducerFunction = Callable[[Context], EventGenerator]
EventHandler = Callable[[Event], EventGenerator]
EventProducer = Callable[[], EventGenerator]