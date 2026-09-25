from unittest.mock import create_autospec
import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
import uuid
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def series_category() -> Category:
    return Category(name="Series")

@pytest.fixture
def category_repository(movie_category, documentary_category, series_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category, series_category]
    )

class TestUpdateGenre:
    # 1. Gênero não encontrado:
    # Tentar atualizar um Genre que não existe deve retornar uma exceção GenreNotFound.
    def test_when_genre_not_exist_then_raise_not_found_exception(
        self,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()

        use_case = UpdateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )
        not_found_id = uuid.uuid4()

        with pytest.raises(GenreNotFound, match="Genre with id .* not found"):
            use_case.execute(request=UpdateGenre.Input(
                id=not_found_id,
                name="New Genre Name",
                category_ids=set(),
                is_active=True
            ))
        

    # 2. Atributos inválidos:
    # Tentar atualizar um Genre passando dados inválidos (ex: nome vazio) deve retornar uma exceção InvalidGenre.
    def test_when_genre_data_is_invalid_then_raise_invalid_genre_exception(
        self,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Original Genre Name")
        genre_repository.save(genre)
        
        use_case = UpdateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(request=UpdateGenre.Input(
                id=genre.id,
                name="",
                category_ids=set(),
                is_active=True
            ))
        
        assert len(genre_repository.list()) == 1
        existing_genre = genre_repository.list()[0]
        assert existing_genre.name == "Original Genre Name"

    # 3. Categorias vinculadas inexistentes:
    # Tentar atualizar um Genre vinculando IDs de categorias que não existem no banco deve retornar uma exceção RelatedCategoriesNotFound.
    def test_when_genre_category_ids_not_exist_then_raise_related_categories_not_found_exception(
        self,
        category_repository,
    ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Original Genre Name")
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories not found: {.*}"):
            use_case.execute(request=UpdateGenre.Input(
                id=genre.id,
                name="Updated Genre Name",
                category_ids={uuid.uuid4(), uuid.uuid4()},
                is_active=True
            ))
        
        assert len(genre_repository.list()) == 1
        existing_genre = genre_repository.list()[0]
        assert existing_genre.name == "Original Genre Name"

    # 4. Atualização com sucesso (Happy Path):
    # Atualizar um Genre com dados válidos e categorias existentes deve persistir as alterações corretamente.
    # Atenção ao comportamento de substituição: Se um Gênero possuía 3 categorias vinculadas e a atualização passar apenas 2, o Gênero deve ficar apenas com essas 2 categorias.
    # Certifique-se de incluir a validação de atributos como name e is_active neste teste.
    def test_when_update_genre_with_valid_data_then_update_successfully(
        self,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        movie_category, documentary_category, series_category = category_repository.list()
        genre = Genre(
            name="Original Genre Name",
            is_active=False,
            categories={
                movie_category.id,
                documentary_category.id,
                series_category.id,
            },
        )
        genre_repository.save(genre)
        updated_category_ids = {
            movie_category.id,
            documentary_category.id,
        }

        use_case = UpdateGenre(
            repository=genre_repository, 
            category_repository=category_repository
        )

        use_case.execute(request=UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre Name",
            category_ids=updated_category_ids,
            is_active=True
        ))

        assert len(genre_repository.list()) == 1
        updated_genre = genre_repository.list()[0]
        assert updated_genre.name == "Updated Genre Name"
        assert updated_genre.is_active is True
        assert updated_genre.categories == updated_category_ids
        assert series_category.id not in updated_genre.categories
