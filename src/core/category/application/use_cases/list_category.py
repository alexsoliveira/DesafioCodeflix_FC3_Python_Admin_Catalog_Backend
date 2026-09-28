from dataclasses import dataclass, field
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta

@dataclass
class ListCategoryRequest:
    order_by: str = "name"
    current_page: int = 1

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListOutput[CategoryOutput]:
        valid_order_by = {"id", "name", "description", "is_active"}

        if request.order_by not in valid_order_by:
            raise ValueError(f"Invalid order_by: {request.order_by}")

        categories = self.repository.list()
        sorted_categories = sorted([
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ], key=lambda category: getattr(category, request.order_by))

        DEFAULT_PAGE_SIZE = 2

        page_offset = (request.current_page - 1) * DEFAULT_PAGE_SIZE
        categories_page = sorted_categories[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return ListOutput[CategoryOutput](
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_categories),
            )
        )

