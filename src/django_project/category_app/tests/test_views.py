from rest_framework import status
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category
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
    CategoryModel.objects.all().delete()
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListAPI:
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
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payloadis_invalid_return_400(self) -> None:
        url = '/api/categories/'
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Categoria para filmes",
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }
        
    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = '/api/categories/'
        response = APIClient().post(
            url,
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = uuid.UUID(response.data["id"])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Filme",
            description="Categoria para filmes",
        )
        assert category_repository.list() == [Category(
            id=created_category_id,
            name="Filme",
            description="Categoria para filmes",
        )]
        
@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = '/api/categories/123123123/'
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Categoria para filmes",
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().put(
            url,
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
                "is_active": True
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Filme"
        assert updated_category.description == "Categoria para filmes"
        assert updated_category.is_active is True

    def test_when_category_not_exists_then_return_404(self):
        url = f'/api/categories/{uuid.uuid4()}/'
        response = APIClient().put(
            url,
            data={
                "name": "Filme",
                "description": "Categoria para filmes",
                "is_active": True
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        url = '/api/categories/123123123/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_does_not_exists_then_return_404(self) -> None:
        url = '/api/categories/{uuid.uuid4()}/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_exists_then_delete_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_movie.id) is None
        assert category_repository.list() == []

@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_payload_partial_exist_name(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                "name": "Filme",
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Filme"
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is True

    def test_when_payload_partial_exist_description(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                "description": "Categoria para filmes",
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == category_movie.name
        assert updated_category.is_active is True
        assert updated_category.description == "Categoria para filmes"

    def test_when_payload_partial_exist_is_active(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == category_movie.name
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is False
        
