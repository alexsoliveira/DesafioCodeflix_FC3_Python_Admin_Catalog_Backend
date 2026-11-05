from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from uuid import UUID

class InMemoryVideoRepository(VideoRepository):
    def __init__(self, videos=None):
        self.videos = videos or []

    def save(self, video):
        self.videos.append(video)

    def get_by_id(self, id:UUID) -> Video | None:
        return next((video for video in self.videos if video.id == id), None)
        # for video in self.videos:
        #     if video.id == id:
        #         return video
        # return None

    def delete(self, id: UUID) -> None:
        video = self.get_by_id(id)
        self.videos.remove(video)

    def update(self, video: Video) -> None:
        old_video = self.get_by_id(video.id)
        if old_video:
            self.videos.remove(old_video)
            self.videos.append(video)

    def list(self) -> list[Video]:
        return [video for video in self.videos]