from dataclasses import dataclass
from pathlib import PurePosixPath
from uuid import UUID

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType
from core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.video_repository import VideoRepository

class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str # "video/mp4"


    def __init__(
            self, 
            video_repository: VideoRepository, 
            storage_service: AbstractStorageService,
            message_bus: AbstractMessageBus
    ):
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.message_bus = message_bus

    def execute(self, input: Input):
        # encontrar nossa entidade
        video = self.video_repository.get_by_id(input.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {input.video_id} not found")

        # upload do nosso arquivo -> storage
        # "/videos/<id>/meuvideo.mp4"
        file_path = PurePosixPath("videos") / str(video.id) / input.file_name
        
        self.storage_service.store(
            file_path=str(file_path),
            content=input.content, 
            content_type=input.content_type
        )
        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )

        # video.upload_video(AudioVideoMedia)
        video.update_video(audio_video_media)

        # persistir essa entidade (com as valores associados)
        self.video_repository.update(video)

        # Apos a transacao terminar (principal / commit)
        # Disparar um evento de integracao
        self.message_bus.handle([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{video.id}.{MediaType.VIDEO}",
                file_path=str(file_path)
            )
        ])

        
        