from unittest.mock import patch

from src.core._shared.events.event import Event
from core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQEventDispatcher


class DummyEvent(Event):
    pass


class TestRabbitMQEventDispatcher:
    def test_default_queue_name(self):
        dispatcher = RabbitMQEventDispatcher()
        assert dispatcher.queue == "video.new"

    def test_custom_queue_name(self):
        dispatcher = RabbitMQEventDispatcher(queue="custom.queue")
        assert dispatcher.queue == "custom.queue"

    def test_dispatch_prints_message(self):
        dispatcher = RabbitMQEventDispatcher()
        event = DummyEvent()

        with patch("builtins.print") as mock_print:
            dispatcher.dispatch(event)

        mock_print.assert_called_once_with(f"Dispatching event to RabbitMQ: {event}")
