from src.core._shared.events.event import Event

class AbstractMessageBus:
    def handle(self, events: list[Event]) -> None:
        raise NotImplementedError