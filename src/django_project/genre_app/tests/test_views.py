from rest_framework.test import APIClient
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from rest_framework import status
import uuid

@pytest.fixture
def category_movie():
    return Category(
        name="Filme",
        description="Categoria para filmes",
    )

@pytest.fixture
def category_documentario():
    return Category(
        name="Documentário",
        description="Categoria para documentários",
    )

@pytest.fixture
def category_repository(category_movie, category_documentario) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_movie)
    repo.save(category_documentario)
    return repo

@pytest.fixture
def genre_romance(category_movie, category_documentario) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories=[category_movie.id, category_documentario.id],
    )

@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self, 
        genre_romance, 
        genre_drama,
        genre_repository,
        category_movie,
        category_documentario,
        category_repository,
    ):
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url = "/api/genres/"
        response = APIClient().get(url)

        # excepted_response = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": "Romance",
        #             "is_active": True,
        #             "categories": [
        #                 str(category_movie.id),
        #                 str(category_documentario.id),
        #             ]
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": "Drama",
        #             "is_active": True,
        #             "categories": []
        #         }
        #     ]
        # }

        assert response.status_code == status.HTTP_200_OK
        # assert response.data == excepted_response

        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == "Romance"
        assert response.data["data"][0]["is_active"] == True
        assert set(response.data["data"][0]["categories"]) == {
            str(category_movie.id), 
            str(category_documentario.id)
        }

        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == "Drama"
        assert response.data["data"][1]["is_active"] == True
        assert response.data["data"][1]["categories"] == [] 
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
        self, 
        genre_repository,
        category_movie,
        category_documentario,
        category_repository,
    ):
        url = "/api/genres/"
        data = {
            "name": "Drama",
            "categories": [
                str(category_movie.id), 
                str(category_documentario.id)
            ],
        }
        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = response.data["id"]

        saved_genre = genre_repository.get_by_id(created_genre_id)
        assert saved_genre.name == "Drama"
        assert saved_genre.categories == {
            category_movie.id, 
            category_documentario.id
        }

    def test_when_payload_is_invalid_then_return_400(self):
        url = "/api/genres/"
        data = {
            "name": "",
            "categories": [],
        }
        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_when_categories_do_not_exist_then_return_400(self):
        url = "/api/genres/"
        category_id = uuid.uuid4()
        data = {
            "name": "Drama",
            "categories": [str(category_id)],
        }
        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories not found" in response.data["error"]
        assert str(category_id) in response.data["error"]

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_does_not_exist_then_raise_404(self):
        url = f"/api/genres/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_pk_is_invalid_then_raise_400(self):
        url = f"/api/genres/123123123/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_genre_from_repository(self, genre_romance, genre_repository):
        genre_repository.save(genre_romance)

        url = f"/api/genres/{genre_romance.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
