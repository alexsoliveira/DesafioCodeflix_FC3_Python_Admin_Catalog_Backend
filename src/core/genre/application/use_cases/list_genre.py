from dataclasses import dataclass
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta

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

        sorted_genres = sorted(
            mapped_genres,
            key=lambda genre: getattr(genre, input.order_by)
        )

        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        genres_page = sorted_genres[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return ListOutput[GenreOutput](
            data=genres_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_genres),
            )
        )
