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
        try:
            genre_model = GenreORM.objects.get(id=id)
        except GenreORM.DoesNotExist:
            return None
        
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()},
        )

    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None
        
        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active
            )
            genre_model.categories.set(genre.categories)

    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories={category.id for category in genre_model.categories.all()},
            )
            for genre_model in GenreORM.objects.all()
        ]