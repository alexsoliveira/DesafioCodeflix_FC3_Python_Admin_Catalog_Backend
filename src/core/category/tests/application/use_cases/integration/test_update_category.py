import uuid
import pytest
from uuid import UUID
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest

class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes"
        )
        
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
            description="Categoria para séries"
        )
        use_case.execute(request=request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == "Série"
        assert updated_category.description == "Categoria para séries"

    def test_can_update_category_name_and_description_and_is_active(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=False
        )

        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
            description="Categoria para séries",
            is_active=True
        )
        use_case.execute(request=request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == "Série"
        assert updated_category.description == "Categoria para séries"
        assert updated_category.is_active == True

    def test_when_category_does_not_exist_should_raise_an_exception(self):
        repository = InMemoryCategoryRepository()
        use_case = UpdateCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = UpdateCategoryRequest(
            id=not_found_id,
            name="Série",
            description="Categoria para séries",
            is_active=True
        )

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request=request)

    def test_create_category_with_invalid_data(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=False
        )

        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="",
            description="Categoria para séries",
            is_active=True
        )

        with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
            use_case.execute(request=request)

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
