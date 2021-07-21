from typing import Callable, Generator, AsyncGenerator, Callable, Any, Union, Optional, Coroutine

Event = Any
Context = Any
EventGenerator = Union[AsyncGenerator[Event, None], Generator[Event, None, Event], Coroutine[None, None, Optional[Event]], Optional[Event]]
FilterFunction = Callable[[Event], bool]
EventHandlerFunction = Union[Callable[[Event, Context], EventGenerator], Callable[[Event], EventGenerator]]
EventProducerFunction = Union[Callable[[Context], EventGenerator], Callable[[], EventGenerator]]
EventHandler = Callable[[Event], EventGenerator]
EventProducer = Callable[[], EventGenerator]