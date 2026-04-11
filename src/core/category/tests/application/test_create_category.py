import pytest
from uuid import UUID
from unittest.mock import MagicMock
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.category_repository import CategoryRepository

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Filme", 
            description="Categoria para filmes",    
            is_active=True,
        )   

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, UUID)
        assert mock_repository.save.called


    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))

        with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
            category_id = use_case.execute(CreateCategoryRequest(name=""))
        
        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"

        
        