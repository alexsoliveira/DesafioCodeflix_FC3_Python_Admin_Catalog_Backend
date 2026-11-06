from unittest.mock import create_autospec

from core._shared.events.event_dispatcher import EventDispatcher
from src.core.video.application.events.handlers import PublishAudioVideoMediaUpdatedHandler
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent


class TestPublishAudioVideoMediaUpdatedHandler:
    def test_handler_dispatches_event_to_event_dispatcher(self):
        mock_dispatcher = create_autospec(EventDispatcher)
        handler = PublishAudioVideoMediaUpdatedHandler(event_dispatcher=mock_dispatcher)

        event = AudioVideoMediaUpdatedIntegrationEvent(
            resource_id="video-123.VIDEO",
            file_path="/videos/video-123/video.mp4",
        )

        handler.handle(event)

        mock_dispatcher.dispatch.assert_called_once_with(event)
