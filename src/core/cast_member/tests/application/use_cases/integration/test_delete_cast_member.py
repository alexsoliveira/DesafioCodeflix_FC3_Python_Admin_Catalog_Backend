import uuid

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
    DeleteCastMemberRequest,
)
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        actor = CastMember(
            id=uuid.uuid4(),
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            id=uuid.uuid4(),
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[actor, director]
        )
        use_case = DeleteCastMember(repository=repository)
        request = DeleteCastMemberRequest(id=actor.id)

        assert repository.get_by_id(actor.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(actor.id) is None
        assert response is None

    def test_when_cast_member_not_found_then_raise_exception(self):
        repository = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(repository=repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMemberRequest(id=uuid.uuid4()))
