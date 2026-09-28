from unittest.mock import create_autospec
import pytest
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
import uuid
from src.core.genre.domain.genre import Genre
from src.core._shared.application.list_output import ListOutput, ListOutputMeta
from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestListGenre:
    def test_list_genres_with_associated_categories(
        self, 
        mock_genre_repository, 
        mock_category_repository_with_categories
    ):             
        genre = Genre(
            name="Drama",
            categories={mock_category_repository_with_categories}
        )
        mock_genre_repository.list.return_value = [genre]

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListOutput(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,    
                    is_active=genre.is_active,
                    categories={mock_category_repository_with_categories}
                )
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=1)
        )

    def test_list_genres_with_no_genres_registered(self):
        mock_genre_repository = create_autospec(GenreRepository)
        mock_genre_repository.list.return_value = []

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListOutput(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))
