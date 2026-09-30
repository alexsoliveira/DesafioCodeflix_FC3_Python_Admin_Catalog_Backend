from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta, sort_and_paginate

@dataclass
class ListCastMemberRequest:
    order_by: str = "name"
    current_page: int = 1

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: ListCastMemberRequest) -> ListOutput[CastMemberOutput]:
        valid_order_by = {"id", "name", "type"}

        if request.order_by not in valid_order_by:
            raise ValueError(f"Invalid order_by: {request.order_by}")

        cast_members = self.repository.list()

        mapped_cast_members = [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
            for cast_member in cast_members
        ]

        DEFAULT_PAGE_SIZE = 2
        return sort_and_paginate(
            items=mapped_cast_members,
            order_by=request.order_by,
            current_page=request.current_page,
            per_page=DEFAULT_PAGE_SIZE,
        )

