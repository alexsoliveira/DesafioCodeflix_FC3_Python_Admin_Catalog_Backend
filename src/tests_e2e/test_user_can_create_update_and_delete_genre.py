import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.models import Genre as GenreModel


@pytest.mark.django_db(transaction=True)
class TestCreateUpdateAndDeleteGenre:
    def setup_method(self):
        GenreModel.objects.all().delete()
        CategoryModel.objects.all().delete()

    def test_user_can_create_update_and_delete_genre(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/genres/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {"data": []}

        category_movie_response = api_client.post(
            "/api/categories/",
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            },
        )
        assert category_movie_response.status_code == status.HTTP_201_CREATED
        category_movie_id = category_movie_response.data["id"]

        category_documentary_response = api_client.post(
            "/api/categories/",
            data={
                "name": "Documentario",
                "description": "Categoria para documentarios",
            },
        )
        assert category_documentary_response.status_code == status.HTTP_201_CREATED
        category_documentary_id = category_documentary_response.data["id"]

        create_response = api_client.post(
            "/api/genres/",
            data={
                "name": "Drama",
                "categories": [
                    str(category_movie_id),
                    str(category_documentary_id),
                ],
            },
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_genre_id = create_response.data["id"]

        list_response = api_client.get("/api/genres/")
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data["data"]) == 1
        listed_genre = list_response.data["data"][0]
        assert listed_genre["id"] == str(created_genre_id)
        assert listed_genre["name"] == "Drama"
        assert listed_genre["is_active"] is True
        assert set(listed_genre["categories"]) == {
            str(category_movie_id),
            str(category_documentary_id),
        }

        update_response = api_client.put(
            f"/api/genres/{created_genre_id}/",
            data={
                "name": "Drama Policial",
                "categories": [str(category_movie_id)],
                "is_active": False,
            },
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/genres/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": str(created_genre_id),
                    "name": "Drama Policial",
                    "is_active": False,
                    "categories": [str(category_movie_id)],
                }
            ]
        }

        delete_response = api_client.delete(f"/api/genres/{created_genre_id}/")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/genres/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {"data": []}
