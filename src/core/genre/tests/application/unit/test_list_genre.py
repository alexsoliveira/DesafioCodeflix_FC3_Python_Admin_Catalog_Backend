from unittest.mock import create_autospec
import pytest
from core.genre.domain.genre_repository import GenreRepository
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
import uuid
from core.genre.domain.genre import Genre
from core.genre.application.use_cases.list_genre import ListGenre, GenreOutput

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

# Escreva os units tests para o use cae, o list genre
# são unit tests bem simples, mas é bom para você ir pegando o jeito e entendendo cada vez mais essa 
# diferença entre os testes de integração que estão utilizando um repositório, ainda que seja um repositório em memória, e os testes unitários que estão utilizando um mock do repositório.
# e os nossos unit tests que estão baseados apenas na interface do nosso repositório.
# Então você vai fazer algo parecido com o que fizemos nos unit tests do create genre. Então fica de exercicio.
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
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,    
                    is_active=genre.is_active,
                    categories={mock_category_repository_with_categories}
                )
            ]
        )

    def test_list_genres_with_no_genres_registered(self):
        mock_genre_repository = create_autospec(GenreRepository)
        mock_genre_repository.list.return_value = []

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])