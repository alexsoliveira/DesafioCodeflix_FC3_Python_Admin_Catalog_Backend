from unittest.mock import create_autospec
import pytest
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
import uuid
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre

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
def series_category() -> Category:
    return Category(name="Series")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category, series_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category, series_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestUpdateGenre:
    # 1. Gênero não encontrado:
    # Tentar atualizar um Genre que não existe deve retornar uma exceção GenreNotFound.
    def test_when_genre_not_exist_then_raise_not_found_exception(
        self,
        mock_genre_repository,
        mock_empty_category_repository
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(
            repository=mock_genre_repository, 
            category_repository=mock_empty_category_repository
        )

        with pytest.raises(GenreNotFound, match="Genre with id .* not found"):
            use_case.execute(request=UpdateGenre.Input(
                id=uuid.uuid4(),
                name="New Genre Name",
                category_ids=set(),
                is_active=True
            ))

        mock_genre_repository.update.assert_not_called()

    # 2. Atributos inválidos:
    # Tentar atualizar um Genre passando dados inválidos (ex: nome vazio) deve retornar uma exceção InvalidGenre.
    def test_when_genre_data_is_invalid_then_raise_invalid_genre_exception(
        self,
        mock_genre_repository,
        mock_empty_category_repository
    ):
        genre = Genre(name="Original Genre Name")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository, 
            category_repository=mock_empty_category_repository
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(request=UpdateGenre.Input(
                id=genre.id,
                name="",
                category_ids=set(),
                is_active=True
            ))

        mock_genre_repository.update.assert_not_called()

    # 3. Categorias vinculadas inexistentes:
    # Tentar atualizar um Genre vinculando IDs de categorias que não existem no banco deve retornar uma exceção RelatedCategoriesNotFound.
    def test_when_genre_category_ids_not_exist_then_raise_related_categories_not_found_exception(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Original Genre Name")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository, 
            category_repository=mock_category_repository_with_categories
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories not found: {.*}"):
            use_case.execute(request=UpdateGenre.Input(
                id=genre.id,
                name="Updated Genre Name",
                category_ids={uuid.uuid4(), uuid.uuid4()},
                is_active=True
            ))

        mock_genre_repository.update.assert_not_called()

    # 4. Atualização com sucesso (Happy Path):
    # Atualizar um Genre com dados válidos e categorias existentes deve persistir as alterações corretamente.
    # Atenção ao comportamento de substituição: Se um Gênero possuía 3 categorias vinculadas e a atualização passar apenas 2, o Gênero deve ficar apenas com essas 2 categorias.
    # Certifique-se de incluir a validação de atributos como name e is_active neste teste.
    def test_when_update_genre_with_valid_data_then_update_successfully(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories
    ):
        movie_category, documentary_category, series_category = (
            mock_category_repository_with_categories.list.return_value
        )
        genre = Genre(
            name="Original Genre Name",
            is_active=False,
            categories={
                movie_category.id,
                documentary_category.id,
                series_category.id,
            },
        )
        mock_genre_repository.get_by_id.return_value = genre
        updated_category_ids = {
            movie_category.id,
            documentary_category.id,
        }

        use_case = UpdateGenre(
            repository=mock_genre_repository, 
            category_repository=mock_category_repository_with_categories
        )

        use_case.execute(request=UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre Name",
            category_ids=updated_category_ids,
            is_active=True
        ))

        mock_genre_repository.update.assert_called_once()
        updated_genre = mock_genre_repository.update.call_args.args[0]
        assert updated_genre.id == genre.id
        assert updated_genre.name == "Updated Genre Name"
        assert updated_genre.is_active is True
        assert updated_genre.categories == updated_category_ids
        assert series_category.id not in updated_genre.categories

    
