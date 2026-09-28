import pytest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, CategoryOutput

class TestListCategory:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListOutput(
            data=[],
            meta=ListOutputMeta(current_page=1, per_page=2, total=0)
        )

    def test_return_existing_categories(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série", 
            description="Categoria para séries",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListOutput(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active  
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    def test_list_categories_order_by_name(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série", 
            description="Categoria para séries",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_serie, category_filme]
        )
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(order_by="name")

        response = use_case.execute(request)

        assert response == ListOutput(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active  
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    def test_list_categories_order_by_description(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série", 
            description="Categoria para séries",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_serie, category_filme]
        )
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(order_by="description")

        response = use_case.execute(request)

        assert response == ListOutput(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active  
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

