from unittest.mock import create_autospec

from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
    def test_when_no_cast_members_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = []

        use_case = ListCastMember(repository=mock_repository)
        request = ListCastMemberRequest()

        response = use_case.execute(request)

        assert response == ListCastMemberResponse(data=[])

    def test_when_cast_members_in_repository_then_return_list(self):
        actor = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR,
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = [actor, director]

        use_case = ListCastMember(repository=mock_repository)
        request = ListCastMemberRequest()

        response = use_case.execute(request)

        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ]
        )
