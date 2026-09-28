from unittest.mock import create_autospec
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, CategoryOutput
from src.core._shared.application.list_output import ListOutput, ListOutputMeta

class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListOutput(
            data=[],
            meta=ListOutputMeta(current_page=1, per_page=2, total=0)
        )

    def test_when_categories_in_repository_then_return_list(self):
        category_filme = Category(
            name="Filme", 
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série", 
            description="Categoria para sÃ©ries",
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [
            category_filme, 
            category_serie
        ]

        use_case = ListCategory(repository=mock_repository)
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

    def test_pagination_and_sorting_with_5_elements(self):
        categories = [
            Category(name="C", description="cat C"),
            Category(name="E", description="cat E"),
            Category(name="A", description="cat A"),
            Category(name="D", description="cat D"),
            Category(name="B", description="cat B"),
        ]
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = categories

        use_case = ListCategory(repository=mock_repository)

        # Page 1
        requestp1 = ListCategoryRequest(current_page=1, order_by="name")
        response_p1 = use_case.execute(requestp1)
        assert len(response_p1.data) == 2
        assert response_p1.data[0].name == "A"
        assert response_p1.data[1].name == "B"
        assert response_p1.meta == ListOutputMeta(current_page=1, per_page=2, total=5)

        # Page 2
        requestp2 = ListCategoryRequest(current_page=2, order_by="name")
        response_p2 = use_case.execute(requestp2)
        assert len(response_p2.data) == 2
        assert response_p2.data[0].name == "C"
        assert response_p2.data[1].name == "D"
        assert response_p2.meta == ListOutputMeta(current_page=2, per_page=2, total=5)

        # Page 3
        requestp3 = ListCategoryRequest(current_page=3, order_by="name")
        response_p3 = use_case.execute(requestp3)
        assert len(response_p3.data) == 1
        assert response_p3.data[0].name == "E"
        assert response_p3.meta == ListOutputMeta(current_page=3, per_page=2, total=5)

