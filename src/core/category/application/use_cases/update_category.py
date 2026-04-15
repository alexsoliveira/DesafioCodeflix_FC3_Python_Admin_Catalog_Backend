import uuid
from uuid import UUID
from dataclasses import dataclass
from core.category.domain.category import Category
from core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData

@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None

class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name
        if request.description is not None:
            current_description = request.description
        
        try:
            category.update_category(
            name=current_name, 
            description=current_description
        )
        except ValueError as err:
            raise InvalidCategoryData(err)

        if request.is_active is True:
            category.activate()
        if request.is_active is False:
            category.deactivate()

        self.repository.update(category)