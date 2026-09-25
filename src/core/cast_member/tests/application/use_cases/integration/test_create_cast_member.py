import pytest
from uuid import UUID

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        request = CreateCastMemberRequest(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert len(repository.cast_members) == 1

        persisted_cast_member = repository.cast_members[0]
        assert persisted_cast_member.id == response.id
        assert persisted_cast_member.name == "Keanu Reeves"
        assert persisted_cast_member.type == CastMemberType.ACTOR

    def test_create_cast_member_with_invalid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMemberData, match="name cannot be empty") as exc_info:
            use_case.execute(
                CreateCastMemberRequest(
                    name="",
                    type=CastMemberType.ACTOR,
                )
            )

        assert exc_info.type is InvalidCastMemberData
        assert str(exc_info.value) == "name cannot be empty"
