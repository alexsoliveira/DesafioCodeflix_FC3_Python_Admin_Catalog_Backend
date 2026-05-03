from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from uuid import UUID
from src.django_project.genre_app.models import Genre as GenreORM
from django.db import transaction

class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre):
        with transaction.atomic():
            genre_model = GenreORM.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active
            )
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, genre: Genre) -> None:
        raise NotImplementedError

    def list(self) -> list[Genre]:
        raise NotImplementedError