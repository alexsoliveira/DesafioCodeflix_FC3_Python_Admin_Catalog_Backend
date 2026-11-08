from unittest.mock import create_autospec
from src.core._shared.application.handler import Handler
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.events.event import Event

class DummyEvent(Event):
    pass

class TestMessageBus:
    def test_calls_correct_handler_with_event(self):
        message_bus = MessageBus()
        dummy_handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler]

        event = DummyEvent()
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)

    def test_calls_all_handlers_when_multiple_handlers_registered(self):
        message_bus = MessageBus()
        dummy_handler_1 = create_autospec(Handler)
        dummy_handler_2 = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler_1, dummy_handler_2]

        event = DummyEvent()
        message_bus.handle([event])

        dummy_handler_1.handle.assert_called_once_with(event)
        dummy_handler_2.handle.assert_called_once_with(event)
