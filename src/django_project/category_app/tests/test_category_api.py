from rest_framework import status
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel
from core.category.domain.category import Category
import pytest
from rest_framework.test import APIClient
from uuid import uuid4
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
def category_repository() -> DjangoORMCategoryRepository:
    """Create repository and clean database before test."""
    from django_project.category_app.models import Category
    Category.objects.all().delete()
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentario: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentario)

        url = '/api/categories/'
        response = APIClient().get(url)

        # expected_data = [
        #     {
        #         "id": str(category_movie.id),
        #         "name": category_movie.name,
        #         "description": category_movie.description,
        #         "is_active": category_movie.is_active
        #     },
        #     {
        #         "id": str(category_documentario.id),
        #         "name": category_documentario.name,
        #         "description": category_documentario.description,
        #         "is_active": category_documentario.is_active
        #     }
        # ]

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                },
                {
                    "id": str(category_documentario.id),
                    "name": category_documentario.name,
                    "description": category_documentario.description,
                    "is_active": category_documentario.is_active
                }
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

@pytest.mark.django_db
class TestRestrieveAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        url = '/api/categories/123123123/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentario: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentario)

        url = f'/api/categories/{category_documentario.id}/'
        response = APIClient().get(url)

        # expected_data = {
        #     "id": str(category_documentario.id),
        #     "name": category_documentario.name,
        #     "description": category_documentario.description,
        #     "is_active": category_documentario.is_active
        # }

        expected_data = {
            "data": {
                "id": str(category_documentario.id),
                "name": category_documentario.name,
                "description": category_documentario.description,
                "is_active": category_documentario.is_active
            }
        } 

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exists(self) -> None:
        url = f'/api/categories/{uuid.uuid4()}/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        

        

