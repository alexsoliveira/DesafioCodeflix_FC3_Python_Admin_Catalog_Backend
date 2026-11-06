from core._shared.events.event_dispatcher import EventDispatcher
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.application.handler import Handler

class PublishAudioVideoMediaUpdatedHandler(Handler):
    def __init__(self, event_dispatcher: EventDispatcher):
        self.event_dispatcher = event_dispatcher

    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        print(f"Publishing event: {event}")
        self.event_dispatcher.dispatch(event)