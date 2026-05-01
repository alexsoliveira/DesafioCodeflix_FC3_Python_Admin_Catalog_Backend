import uuid
from uuid import UUID
from dataclasses import dataclass, field
from core.genre.domain.genre import Genre
from core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound

class UpdateGenre:
    def __init__(self, repository, category_repository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        category_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True

    def execute(self, request: Input) -> None:
        genre = self.repository.get_by_id(request.id)

        if genre is None:
            raise GenreNotFound(f"Genre with id {request.id} not found")

        current_name = genre.name

        if request.name is not None:
            current_name = request.name
        
        category_ids = {category.id for category in self.category_repository.list() }
        if not request.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {request.category_ids - category_ids}"
            )
        
        try:
             genre = Genre(
                name=request.name,
                 id=request.id,
                is_active=request.is_active,
                categories=request.category_ids,
            )
        except ValueError as e:
            raise InvalidGenre(str(e))

        if request.is_active is True:
            genre.activate()
        if request.is_active is False:
            genre.deactivate()

        self.repository.update(genre)