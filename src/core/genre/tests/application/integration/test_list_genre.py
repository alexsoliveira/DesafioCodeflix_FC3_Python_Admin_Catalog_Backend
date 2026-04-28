
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.genre.application.use_cases.list_genre import ListGenre, GenreOutput

class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()
        movie_category = Category(name="Movie")
        category_repository.save(movie_category)

        documentary_category = Category(name="Documentary")
        category_repository.save(documentary_category)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,    
                    is_active=genre.is_active,
                    categories={movie_category.id, documentary_category.id}
                )
            ]
        )

    # Criar um novo teste, quando não tenha nenhum gênero registrado. Então um repositorio vazio.