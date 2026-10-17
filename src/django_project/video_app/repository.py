from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objects import (
    AudioVideoMedia,
    ImageMedia,
    MediaStatus,
    Rating,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import (
    AudioVideoMedia as AudioVideoMediaORM,
    ImageMedia as ImageMediaORM,
    Video as VideoORM,
)


class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video):
        with transaction.atomic():
            video_model = VideoORM.objects.create(
                id=video.id,
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                duration=video.duration,
                published=video.published,
                opened=video.opened,
                rating=self._rating_name(video.rating),
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None

        return self._to_entity(video_model)

    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        with transaction.atomic():
            VideoORM.objects.filter(id=video.id).update(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                duration=video.duration,
                published=video.published,
                opened=video.opened,
                rating=self._rating_name(video.rating),
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def list(self) -> list[Video]:
        return [self._to_entity(video_model) for video_model in VideoORM.objects.all()]

    @staticmethod
    def _rating_name(rating: Rating | str) -> str:
        return rating.name if isinstance(rating, Rating) else rating

    @staticmethod
    def _image_media(model: ImageMediaORM | None) -> ImageMedia | None:
        if model is None:
            return None
        return ImageMedia(
            checksum=model.checksum,
            name=model.name,
            location=model.raw_location,
        )

    @staticmethod
    def _audio_video_media(model: AudioVideoMediaORM | None) -> AudioVideoMedia | None:
        if model is None:
            return None
        return AudioVideoMedia(
            checksum=model.checksum,
            name=model.name,
            raw_location=model.raw_location,
            encoded_location=model.encoded_location,
            status=MediaStatus[model.status],
        )

    @classmethod
    def _to_entity(cls, video_model: VideoORM) -> Video:
        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            duration=video_model.duration,
            published=video_model.published,
            opened=video_model.opened,
            rating=Rating[video_model.rating],
            categories={category.id for category in video_model.categories.all()},
            genres={genre.id for genre in video_model.genres.all()},
            cast_members={cast_member.id for cast_member in video_model.cast_members.all()},
            banner=cls._image_media(video_model.banner),
            thumbnail=cls._image_media(video_model.thumbnail),
            thumbnail_half=cls._image_media(video_model.thumbnail_half),
            trailer=cls._audio_video_media(video_model.trailer),
            video=cls._audio_video_media(video_model.video),
        )