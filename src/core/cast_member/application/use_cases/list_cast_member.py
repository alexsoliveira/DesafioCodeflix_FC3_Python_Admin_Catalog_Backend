from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core._shared.application.list_output import ListOutput, ListOutputMeta

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

        sorted_cast_members = sorted(
            mapped_cast_members,
            key=lambda cast_member: getattr(cast_member, request.order_by)
        )

        DEFAULT_PAGE_SIZE = 2
        page_offset = (request.current_page - 1) * DEFAULT_PAGE_SIZE
        cast_members_page = sorted_cast_members[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return ListOutput[CastMemberOutput](
            data=cast_members_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_cast_members),
            )
        )

