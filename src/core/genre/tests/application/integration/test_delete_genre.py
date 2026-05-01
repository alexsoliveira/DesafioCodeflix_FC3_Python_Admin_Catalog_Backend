from unittest.mock import create_autospec
import pytest
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.domain.genre import Genre
import uuid
from src.core.genre.application.exceptions import GenreNotFound

class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Romance")
        genre_repository.save(genre)

        use_case = DeleteGenre(repository=genre_repository)
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        assert genre_repository.get_by_id(genre.id) is None

    def test_when_genre_not_exist_then_raise_not_found_exception(
        self
    ):
        genre_repository = InMemoryGenreRepository()

        use_case = DeleteGenre(repository=genre_repository)

        with pytest.raises(GenreNotFound, match="Genre with id .* not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))

        assert genre_repository.get_by_id(uuid.uuid4()) is None