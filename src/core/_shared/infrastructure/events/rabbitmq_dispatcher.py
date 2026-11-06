from dataclasses import asdict
import json
import pika

from src.core._shared.events.event_dispatcher import EventDispatcher
from src.core._shared.events.event import Event

class RabbitMQEventDispatcher(EventDispatcher):
    """
    docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    """
    def __init__(self, host="localhost", queue="videos.new") -> None:
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def dispatch(self, event: Event) -> None:
        # Aqui você implementaria a lógica para enviar o evento para o RabbitMQ
        if not self.connection:
            # Simulando a criação de uma conexão e canal com o RabbitMQ
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(
            exchange='', 
            routing_key=self.queue, 
            body=json.dumps(asdict(event)),
        )
        print(f"Sent {event} to queue {self.queue}")

    def close(self):
        self.connection.close()
    