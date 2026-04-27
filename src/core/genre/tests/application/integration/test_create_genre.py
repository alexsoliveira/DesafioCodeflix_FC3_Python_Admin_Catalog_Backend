from unittest.mock import create_autospec
import pytest
from core.genre.domain.genre_repository import GenreRepository
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
import uuid
from core.genre.domain.genre import Genre
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )

class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={uuid.uuid4(), uuid.uuid4()}
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        for category_id in input.category_ids:
            assert str(category_id) in str(exc_info.value)

    def test_create_genre_without_categories(
        self,
        movie_category,
        documentary_category,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids=set()
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True
        
        
        