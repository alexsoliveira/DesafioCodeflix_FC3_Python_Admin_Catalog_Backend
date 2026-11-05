from typing import Type

from src.core._shared.application.handler import Handler
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event

class MessageBus(AbstractMessageBus):
    def __init__(self):
        self.handlers: dict[Type[Event], list[Handler]] = {}

    def handle(self, events: list[Event]) -> None:
        for event in events:
            for handler in self.handlers[type(event)]:
                handler.handle(event)

    # def register(self, event_type: Type[Event], handler: Handler) -> None:
    #     self.handlers.setdefault(event_type, []).append(handler)