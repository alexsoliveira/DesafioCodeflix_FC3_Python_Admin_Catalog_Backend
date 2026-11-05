from abc import ABC, abstractmethod
from src.core._shared.events.event import Event

class Handler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        pass