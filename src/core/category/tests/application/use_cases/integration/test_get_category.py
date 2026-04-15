import pytest
import uuid
from uuid import UUID
from unittest.mock import MagicMock
from core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from core.category.application.use_cases.exceptions import InvalidCategoryData, CategoryNotFound
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.category.domain.category import Category

class TestGetCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=category_filme.id
        )

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name=category_filme.name,
            description=category_filme.description,
            is_active=category_filme.is_active,
        )

    def test_when_category_does_not_exist_should_raise_an_exception(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(
            id=not_found_id
        )

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        
        