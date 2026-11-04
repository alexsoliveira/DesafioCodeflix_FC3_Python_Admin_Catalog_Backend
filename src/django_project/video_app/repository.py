from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objects import (
    AudioVideoMedia,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import (
    AudioVideoMedia as AudioVideoMediaORM,
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
                rating=video.rating,
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(pk=id)
            return Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                launch_year=video_model.launch_year,
                duration=video_model.duration,
                published=video_model.published,
                opened=video_model.opened,
                rating=video_model.rating,
                categories=set(video_model.categories.values_list('id', flat=True)),
                genres=set(video_model.genres.values_list('id', flat=True)),
                cast_members=set(video_model.cast_members.values_list('id', flat=True)),
            )
        except VideoORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(pk=id).delete()

    def list(self) -> list[Video]:
        video_models = VideoORM.objects.all()
        return [
            Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                launch_year=video_model.launch_year,
                duration=video_model.duration,
                published=video_model.published,
                opened=video_model.opened,
                rating=video_model.rating,
                categories=set(video_model.categories.values_list('id', flat=True)),
                genres=set(video_model.genres.values_list('id', flat=True)),
                cast_members=set(video_model.cast_members.values_list('id', flat=True)),
            )
            for video_model in video_models
        ]

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:        
            # Buscar e deletar video medias associadas
            AudioVideoMedia.objects.filter(video_id=video.id).delete()

            # Atualiza relationships
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

            # Persistir o Value Object
            video_model.video = AudioVideoMediaORM.objects.create(
                name=video.video.name,
                raw_location=video.video.raw_location,
                encoded_location=video.video.encoded_location,
                status=video.video.status,
            )

            # Atualizar os atributos do Video
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.opened = video.opened
            video_model.duration = video.duration
            video_model.rating = video.rating
            video_model.published = video.published

            video_model.save()