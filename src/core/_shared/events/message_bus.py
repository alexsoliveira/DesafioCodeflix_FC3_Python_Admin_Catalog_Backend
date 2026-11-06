from typing import Type

from core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQEventDispatcher
from src.core.video.application.events.handlers import PublishAudioVideoMediaUpdatedHandler
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.application.handler import Handler
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event

class MessageBus(AbstractMessageBus):
    def __init__(self):
        self.handlers: dict[Type[Event], list[Handler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdatedHandler(
                    event_dispatcher=RabbitMQEventDispatcher(queue="videos.new")
                ),
            ],
        }

    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(e)

    # def register(self, event_type: Type[Event], handler: Handler) -> None:
    #     self.handlers.setdefault(event_type, []).append(handler)