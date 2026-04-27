from core.genre.domain.genre_repository import GenreRepository
from core.genre.domain.genre import Genre
from uuid import UUID

class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres=None):
        self.genres = genres or []

    def save(self, genre):
        self.genres.append(genre)

    def get_by_id(self, id:UUID) -> Genre | None:
        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        self.genres.remove(genre)

    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id)
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(genre)

    def list(self) -> list[Genre]:
        return [genre for genre in self.genres]