from unittest.mock import create_autospec

from src.core._shared.application.list_output import ListOutput, ListOutputMeta
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberRequest,
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

        assert response == ListOutput(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))

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

        assert response == ListOutput(
            data=[
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    def test_pagination_and_sorting_with_5_elements(self):
        cast_members = [
            CastMember(name="C", type=CastMemberType.ACTOR),
            CastMember(name="E", type=CastMemberType.ACTOR),
            CastMember(name="A", type=CastMemberType.ACTOR),
            CastMember(name="D", type=CastMemberType.ACTOR),
            CastMember(name="B", type=CastMemberType.ACTOR),
        ]
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = cast_members

        use_case = ListCastMember(repository=mock_repository)

        # Page 1
        requestp1 = ListCastMemberRequest(current_page=1, order_by="name")
        response_p1 = use_case.execute(requestp1)
        assert len(response_p1.data) == 2
        assert response_p1.data[0].name == "A"
        assert response_p1.data[1].name == "B"
        assert response_p1.meta == ListOutputMeta(current_page=1, per_page=2, total=5)

        # Page 2
        requestp2 = ListCastMemberRequest(current_page=2, order_by="name")
        response_p2 = use_case.execute(requestp2)
        assert len(response_p2.data) == 2
        assert response_p2.data[0].name == "C"
        assert response_p2.data[1].name == "D"
        assert response_p2.meta == ListOutputMeta(current_page=2, per_page=2, total=5)

        # Page 3
        requestp3 = ListCastMemberRequest(current_page=3, order_by="name")
        response_p3 = use_case.execute(requestp3)
        assert len(response_p3.data) == 1
        assert response_p3.data[0].name == "E"
        assert response_p3.meta == ListOutputMeta(current_page=3, per_page=2, total=5)

