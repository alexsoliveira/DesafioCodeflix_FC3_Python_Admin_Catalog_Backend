from dataclasses import dataclass
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta, sort_and_paginate

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    def execute(self, input: Input) -> ListOutput[GenreOutput]:
        valid_order_by = {"id", "name", "is_active"}

        if input.order_by not in valid_order_by:
            raise ValueError(f"Invalid order_by: {input.order_by}")

        genres = self.repository.list()
        
        mapped_genres = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories
            ) for genre in genres
        ]

        DEFAULT_PAGE_SIZE = 2
        return sort_and_paginate(
            items=mapped_genres,
            order_by=input.order_by,
            current_page=input.current_page,
            per_page=DEFAULT_PAGE_SIZE,
        )
