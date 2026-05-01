from unittest.mock import create_autospec
import pytest
from core.genre.application.use_cases.delete_genre import DeleteGenre
from core.genre.domain.genre_repository import GenreRepository
from core.genre.domain.genre import Genre
import uuid
from core.genre.application.exceptions import GenreNotFound

@pytest.fixture
def mock_genre_repository():
    return create_autospec(GenreRepository)

class TestDeleteGenre:
    def test_delete_genre_from_repository(
        self,
        mock_genre_repository
    ):
        genre = Genre(name="Romance")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(repository=mock_genre_repository)
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        mock_genre_repository.delete.assert_called_once_with(id=genre.id)

    def test_when_genre_not_exist_then_raise_not_found_exception(
        self,
        mock_genre_repository
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = DeleteGenre(repository=mock_genre_repository)

        with pytest.raises(GenreNotFound, match="Genre with id .* not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))

        mock_genre_repository.delete.assert_not_called()