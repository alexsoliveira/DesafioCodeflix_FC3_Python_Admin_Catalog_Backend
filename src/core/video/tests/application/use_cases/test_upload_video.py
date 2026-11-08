from unittest.mock import create_autospec

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from src.core.video.domain.video import Video

class TestUploadVideo:
    def test_upload_video_media_to_video(self):
        # Existe uma entidade de video
        # Passo um arquivo para o usecase
        # O arquivo é salvo no storage
        # Video seja atualizado com a media
        video = Video(
            title="Meu video",
            description="Descricao qualquer",
            launch_year=2024,
            duration=120,
            rating=Rating.L,
            published=False,
            opened=False,
            categories=set(),
            genres=set(),
            cast_members=set()
        )

        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        )
        input = UploadVideo.Input(
            video_id=video.id,
            file_name="video.mp4",
            content=b"conteudo do arquivo",
            content_type="video/mp4"
        )
        use_case.execute(input=input)

        mock_storage.store.assert_called_once_with(
            file_path=f"videos/{video.id}/video.mp4",
            content=b"conteudo do arquivo",
            content_type="video/mp4"
        )
        assert video.video == AudioVideoMedia(
            name="video.mp4",
            raw_location=f"videos/{video.id}/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )

        assert video_repository.videos[0] == video
        mock_message_bus.handle.assert_called_once_with(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{video.id}.{MediaType.VIDEO}",
                    file_path=f"videos/{video.id}/video.mp4"
                )
            ]
        )

    def test_when_video_does_not_exist_then_raise_error(self):
        video_repository = InMemoryVideoRepository(videos=[])
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(AbstractMessageBus)

        use_case = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        )
        input = UploadVideo.Input(
            video_id="non-existent-id",
            file_name="video.mp4",
            content=b"conteudo do arquivo",
            content_type="video/mp4"
        )
        try:
            use_case.execute(input=input)
        except Exception as e:
            assert str(e) == "Video with id non-existent-id not found"