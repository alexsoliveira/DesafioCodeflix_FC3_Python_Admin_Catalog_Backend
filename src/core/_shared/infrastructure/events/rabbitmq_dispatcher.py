from core._shared.events.event_dispatcher import EventDispatcher
from src.core._shared.events.event import Event

class RabbitMQEventDispatcher(EventDispatcher):
    def __init__(self, queue="video.new") -> None:
        self.queue = queue
    def dispatch(self, event: Event) -> None:
        # Aqui você implementaria a lógica para enviar o evento para o RabbitMQ
        print(f"Dispatching event to RabbitMQ: {event}")
    