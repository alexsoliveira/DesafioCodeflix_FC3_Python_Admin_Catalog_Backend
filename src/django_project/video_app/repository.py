from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from uuid import UUID
from src.django_project.video_app.models import Video as VideoORM
from django.db import transaction

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
                rating=video.rating
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None

        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            launch_year=video_model.launch_year,
            duration=video_model.duration,
            published=video_model.published,
            rating=video_model.rating,
            categories={category.id for category in video_model.categories.all()},
            genres={genre.id for genre in video_model.genres.all()},
            cast_members={cast_member.id for cast_member in video_model.cast_members.all()},
            banner=video_model.banner,
            thumbnail=video_model.thumbnail,
            thumbnail_half=video_model.thumbnail_half,
            trailer=video_model.trailer,
            video=video_model.video
        )

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
                rating=video.rating
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def list(self) -> list[Video]:
        return [
            Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                launch_year=video_model.launch_year,
                duration=video_model.duration,
                published=video_model.published,
                rating=video_model.rating,
                categories={category.id for category in video_model.categories.all()},
                genres={genre.id for genre in video_model.genres.all()},
                cast_members={cast_member.id for cast_member in video_model.cast_members.all()},
                banner=video_model.banner,
                thumbnail=video_model.thumbnail,
                thumbnail_half=video_model.thumbnail_half,
                trailer=video_model.trailer,
                video=video_model.video
            )
            for video_model in VideoORM.objects.all()
        ]