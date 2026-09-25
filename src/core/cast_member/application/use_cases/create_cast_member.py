from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CreateCastMemberRequest:
    name: str
    type: CastMemberType


@dataclass
class CreateCastMemberResponse:
    id: UUID


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: CreateCastMemberRequest) -> CreateCastMemberResponse:
        try:
            cast_member = CastMember(
                name=request.name,
                type=request.type,
            )
        except ValueError as err:
            raise InvalidCastMemberData(err)

        self.repository.save(cast_member)
        return CreateCastMemberResponse(id=cast_member.id)
