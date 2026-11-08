from django.core.management.base import BaseCommand

from src.core.video.infra.video_converted_consumer import VideoConvertedRabbitMQConsumer

class Command(BaseCommand):
    help = 'Start the consumer to process the converted videos'

    def handle(self, *args, **kwargs):
        consumer = VideoConvertedRabbitMQConsumer()
        consumer.start()