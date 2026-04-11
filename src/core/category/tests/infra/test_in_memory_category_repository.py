
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme", 
            description="Categoria para filmes"
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetById:
    def test_can_get_category_by_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme", 
            description="Categoria para filmes"
        )
        repository.save(category)

        found_category = repository.get_by_id(category.id)

        assert found_category == category
        assert found_category.id == category.id
        assert found_category.name == category.name
        assert found_category.description == category.description
        assert found_category.is_active == category.is_active

class TestDelete:
    def test_can_delete_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme", 
            description="Categoria para filmes"
        )
        repository.save(category)

        repository.delete(category.id)

        assert len(repository.categories) == 0