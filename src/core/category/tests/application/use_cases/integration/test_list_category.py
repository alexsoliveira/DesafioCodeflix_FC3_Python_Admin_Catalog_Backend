from unittest.mock import create_autospec

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse, CategoryOutput
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestListCategory:
    def test_return_empty_list(self):
        category = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série", 
            description="Categoria para séries",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category_filme)
        repository.save(category_serie)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
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
            ]
        )

    def test_list_categories_order_by_name(self):
        category_movie = Category(
            name="Movie", 
            description="Category for movies",
        )
        category_documentary = Category(
            name="Documentary", 
            description="Category for documentaries",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(order_by="name")

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active
                ),
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active  
                ),
            ]
        )

    def test_list_categories_order_by_description(self):
        category_movie = Category(
            name="Movie", 
            description="Category for movies",
        )
        category_documentary = Category(
            name="Documentary", 
            description="Category for documentaries",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(order_by="description")

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
                    data=[
                        CategoryOutput(
                            id=category_documentary.id,
                            name=category_documentary.name,
                            description=category_documentary.description,
                            is_active=category_documentary.is_active
                        ),
                        CategoryOutput(
                            id=category_movie.id,
                            name=category_movie.name,
                            description=category_movie.description,
                            is_active=category_movie.is_active  
                        ),
                    ]
                )

    def test_list_categories_with_invalid_order_by(self):
        category_movie = Category(
            name="Movie",
            description="Category for movies",
        )
        category_documentary = Category(
            name="Documentary",
            description="Category for documentaries",
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest(order_by="idade")

        with pytest.raises(ValueError, match="Invalid order_by: idade"):
            use_case.execute(request)

        
        