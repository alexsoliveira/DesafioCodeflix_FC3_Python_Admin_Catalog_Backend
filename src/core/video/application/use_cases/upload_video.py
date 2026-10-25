from dataclasses import dataclass
from pathlib import PurePosixPath
from uuid import UUID

from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.application.exceptions import VideoNotFound
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
            storage_service: AbstractStorageService
    ):
        self.video_repository = video_repository
        self.storage_service = storage_service

    def execute(self, input: Input):
        # encontrar nossa entidade
        video = self.video_repository.get_by_id(input.video_id)
        if video is None:
            raise VideoNotFound(input.video_id)

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
        )

        # video.upload_video(AudioVideoMedia)
        video.update_video(audio_video_media)

        # persistir essa entidade (com as valores associados)
        self.video_repository.update(video)  

        
        