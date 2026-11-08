from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.use_cases.exceptions import MediaNotFound, VideoNotFound
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.value_objects import MediaStatus, MediaType

class ProcessAudioVideoMedia:

    @dataclass
    class Input:
        encoded_location: str
        video_id: UUID
        status: MediaStatus
        media_type: MediaType

    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
    
    def execute(self, request: Input):
        video = self.video_repository.get_by_id(id=request.video_id)

        if video is None:
            raise VideoNotFound(f"Video with id {request.video_id} not found.")

        if request.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have media to be processed")
            video.process_video(status=request.status, encoded_location=request.encoded_location)
        elif request.media_type == MediaType.TRAILER:
            if not video.trailer:
                raise MediaNotFound("Trailer must have media to be processed")
            video.process_trailer(status=request.status, encoded_location=request.encoded_location)
            
        self.video_repository.update(video)
