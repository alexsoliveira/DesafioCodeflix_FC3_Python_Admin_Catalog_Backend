from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberRequest,
    ListCastMemberResponse,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    def test_return_empty_list(self):
        repository = InMemoryCastMemberRepository(cast_members=[])

        use_case = ListCastMember(repository=repository)
        request = ListCastMemberRequest()

        response = use_case.execute(request)

        assert response == ListCastMemberResponse(data=[])

    def test_return_existing_cast_members(self):
        actor = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        director = CastMember(
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository()
        repository.save(actor)
        repository.save(director)

        use_case = ListCastMember(repository=repository)
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
