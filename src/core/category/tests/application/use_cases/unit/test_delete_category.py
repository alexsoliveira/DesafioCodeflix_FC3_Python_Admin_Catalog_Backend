import uuid
from uuid import UUID
from core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from core.category.domain.category_repository import CategoryRepository
from core.category.domain.category import Category
from unittest.mock import create_autospec
from core.category.application.use_cases.exceptions import CategoryNotFound
import pytest

class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filme", 
            description="Categoria para filmes",
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(repository=mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=mock_repository)

        with pytest.raises(CategoryNotFound):
            use_case.execute(DeleteCategoryRequest(id=uuid.uuid4()))

        mock_repository.delete.assert_not_called()