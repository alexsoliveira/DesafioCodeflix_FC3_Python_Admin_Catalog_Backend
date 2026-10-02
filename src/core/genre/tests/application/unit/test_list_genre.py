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

    def test_pagination_and_sorting_with_5_elements(self):
        genres = [
            Genre(name="C"),
            Genre(name="E"),
            Genre(name="A"),
            Genre(name="D"),
            Genre(name="B"),
        ]
        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = genres

        use_case = ListGenre(repository=mock_repository)

        # Page 1
        requestp1 = ListGenre.Input(current_page=1, order_by="name")
        response_p1 = use_case.execute(requestp1)
        assert len(response_p1.data) == 2
        assert response_p1.data[0].name == "A"
        assert response_p1.data[1].name == "B"
        assert response_p1.meta == ListOutputMeta(current_page=1, per_page=2, total=5)

        # Page 2
        requestp2 = ListGenre.Input(current_page=2, order_by="name")
        response_p2 = use_case.execute(requestp2)
        assert len(response_p2.data) == 2
        assert response_p2.data[0].name == "C"
        assert response_p2.data[1].name == "D"
        assert response_p2.meta == ListOutputMeta(current_page=2, per_page=2, total=5)

        # Page 3
        requestp3 = ListGenre.Input(current_page=3, order_by="name")
        response_p3 = use_case.execute(requestp3)
        assert len(response_p3.data) == 1
        assert response_p3.data[0].name == "E"
        assert response_p3.meta == ListOutputMeta(current_page=3, per_page=2, total=5)
