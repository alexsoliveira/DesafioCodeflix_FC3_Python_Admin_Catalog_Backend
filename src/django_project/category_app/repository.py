from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryORM
from src.core.category.domain.category import Category

class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryORM | None = None):
        self.model = model or CategoryORM

    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
        # self.model.objects.create(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     is_active=category.is_active,
        # )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
            # return Category(
            #     id=category.id,
            #     name=category.name,
            #     description=category.description,
            #     is_active=category.is_active,
            # )
        except self.model.DoesNotExist:
            return None
        
    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        return [
            # Category(
            #     id=category.id,
            #     name=category.name,
            #     description=category.description,
            #     is_active=category.is_active,
            # )
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.model.objects.all()   
        ]
    
    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryORM:
        return CategoryORM(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def to_entity(category_orm: CategoryORM) -> Category:
        return Category(
            id=category_orm.id,
            name=category_orm.name,
            description=category_orm.description,
            is_active=category_orm.is_active,
        )