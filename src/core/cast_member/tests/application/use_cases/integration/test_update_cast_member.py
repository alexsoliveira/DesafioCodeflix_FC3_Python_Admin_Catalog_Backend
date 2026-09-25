import uuid

import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberRequest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestUpdateCastMember:
    def test_can_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Lana Wachowski",
            type=CastMemberType.DIRECTOR,
        )
        use_case.execute(request=request)

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Lana Wachowski"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_when_cast_member_does_not_exist_should_raise_an_exception(self):
        repository = InMemoryCastMemberRepository()
        use_case = UpdateCastMember(repository=repository)
        not_found_id = uuid.uuid4()
        request = UpdateCastMemberRequest(
            id=not_found_id,
            name="Lana Wachowski",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(request=request)

    def test_update_cast_member_with_invalid_data(self):
        cast_member = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(InvalidCastMemberData, match="name cannot be empty") as exc_info:
            use_case.execute(request=request)

        assert exc_info.type is InvalidCastMemberData
        assert str(exc_info.value) == "name cannot be empty"
