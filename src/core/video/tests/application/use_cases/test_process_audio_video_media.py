from decimal import Decimal
import uuid
import pytest

from src.core.video.application.use_cases.exceptions import MediaNotFound, VideoNotFound
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()


@pytest.fixture
def video_with_media() -> Video:
    return Video(
        id=uuid.uuid4(),
        title="The Matrix",
        description="Sci-fi classic",
        launch_year=1999,
        duration=Decimal("136.0"),
        rating=Rating.AGE_14,
        categories=set(),
        genres=set(),
        cast_members=set(),
        video=AudioVideoMedia(
            name="matrix.mp4",
            raw_location="/raw/matrix.mp4",
            encoded_location="",
            status=MediaStatus.PROCESSING,
            media_type=MediaType.VIDEO,
        ),
        trailer=AudioVideoMedia(
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="",
            status=MediaStatus.PROCESSING,
            media_type=MediaType.TRAILER,
        ),
    )


class TestProcessAudioVideoMedia:
    def test_raises_exception_when_video_not_found(
        self,
        video_repository: InMemoryVideoRepository,
    ):
        use_case = ProcessAudioVideoMedia(video_repository=video_repository)
        non_existent_id = uuid.uuid4()

        with pytest.raises(VideoNotFound, match=f"Video with id {non_existent_id} not found."):
            use_case.execute(
                request=ProcessAudioVideoMedia.Input(
                    video_id=non_existent_id,
                    encoded_location="/encoded/matrix.mp4",
                    status=MediaStatus.COMPLETED,
                    media_type=MediaType.VIDEO,
                )
            )

    def test_raises_exception_when_video_has_no_video_media(
        self,
        video_repository: InMemoryVideoRepository,
    ):
        video = Video(
            id=uuid.uuid4(),
            title="The Matrix",
            description="Sci-fi classic",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video=None,
        )
        video_repository.save(video)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)

        with pytest.raises(MediaNotFound, match="Video must have media to be processed"):
            use_case.execute(
                request=ProcessAudioVideoMedia.Input(
                    video_id=video.id,
                    encoded_location="/encoded/matrix.mp4",
                    status=MediaStatus.COMPLETED,
                    media_type=MediaType.VIDEO,
                )
            )

    def test_raises_exception_when_video_has_no_trailer_media(
        self,
        video_repository: InMemoryVideoRepository,
    ):
        video = Video(
            id=uuid.uuid4(),
            title="The Matrix",
            description="Sci-fi classic",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
            trailer=None,
        )
        video_repository.save(video)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)

        with pytest.raises(MediaNotFound, match="Trailer must have media to be processed"):
            use_case.execute(
                request=ProcessAudioVideoMedia.Input(
                    video_id=video.id,
                    encoded_location="/encoded/trailer.mp4",
                    status=MediaStatus.COMPLETED,
                    media_type=MediaType.TRAILER,
                )
            )

    def test_process_video_media_completed(
        self,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ):
        video_repository.save(video_with_media)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)
        use_case.execute(
            request=ProcessAudioVideoMedia.Input(
                video_id=video_with_media.id,
                encoded_location="/encoded/matrix.mp4",
                status=MediaStatus.COMPLETED,
                media_type=MediaType.VIDEO,
            )
        )

        saved_video = video_repository.get_by_id(video_with_media.id)
        assert saved_video is not None
        assert saved_video.video.status == MediaStatus.COMPLETED
        assert saved_video.video.encoded_location == "/encoded/matrix.mp4"
        assert saved_video.published is True

    def test_process_video_media_error(
        self,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ):
        video_repository.save(video_with_media)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)
        use_case.execute(
            request=ProcessAudioVideoMedia.Input(
                video_id=video_with_media.id,
                encoded_location="/encoded/matrix.mp4",
                status=MediaStatus.ERROR,
                media_type=MediaType.VIDEO,
            )
        )

        saved_video = video_repository.get_by_id(video_with_media.id)
        assert saved_video is not None
        assert saved_video.video.status == MediaStatus.ERROR
        assert saved_video.video.encoded_location == ""
        assert saved_video.published is False

    def test_process_trailer_media_completed(
        self,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ):
        video_repository.save(video_with_media)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)
        use_case.execute(
            request=ProcessAudioVideoMedia.Input(
                video_id=video_with_media.id,
                encoded_location="/encoded/trailer.mp4",
                status=MediaStatus.COMPLETED,
                media_type=MediaType.TRAILER,
            )
        )

        saved_video = video_repository.get_by_id(video_with_media.id)
        assert saved_video is not None
        assert saved_video.trailer.status == MediaStatus.COMPLETED
        assert saved_video.trailer.encoded_location == "/encoded/trailer.mp4"
        assert saved_video.published is False

    def test_process_trailer_media_error(
        self,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ):
        video_repository.save(video_with_media)

        use_case = ProcessAudioVideoMedia(video_repository=video_repository)
        use_case.execute(
            request=ProcessAudioVideoMedia.Input(
                video_id=video_with_media.id,
                encoded_location="/encoded/trailer.mp4",
                status=MediaStatus.ERROR,
                media_type=MediaType.TRAILER,
            )
        )

        saved_video = video_repository.get_by_id(video_with_media.id)
        assert saved_video is not None
        assert saved_video.trailer.status == MediaStatus.ERROR
        assert saved_video.trailer.encoded_location == ""
        assert saved_video.published is False
