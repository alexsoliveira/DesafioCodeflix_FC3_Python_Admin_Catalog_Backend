import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(
        name="Keanu Reeves",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(
        name="Lana Wachowski",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    CastMemberModel.objects.all().delete()
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        actor_cast_member: CastMember,
        director_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor_cast_member)
        cast_member_repository.save(director_cast_member)

        response = APIClient().get("/api/cast_members/")

        expected_data = {
            "data": [
                {
                    "id": str(actor_cast_member.id),
                    "name": actor_cast_member.name,
                    "type": actor_cast_member.type.value,
                },
                {
                    "id": str(director_cast_member.id),
                    "name": director_cast_member.name,
                    "type": director_cast_member.type.value,
                },
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "",
                "type": "WRITER",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "type": ['"WRITER" is not a valid choice.'],
        }

    def test_when_payload_is_valid_then_create_cast_member_and_return_201(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "Keanu Reeves",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_cast_member_id = uuid.UUID(response.data["id"])
        assert cast_member_repository.get_by_id(created_cast_member_id) == CastMember(
            id=created_cast_member_id,
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        assert cast_member_repository.list() == [
            CastMember(
                id=created_cast_member_id,
                name="Keanu Reeves",
                type=CastMemberType.ACTOR,
            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        response = APIClient().put(
            "/api/cast_members/123123123/",
            data={
                "name": "",
                "type": "WRITER",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "type": ['"WRITER" is not a valid choice.'],
        }

    def test_when_payload_is_valid_then_update_cast_member_and_return_204(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor_cast_member)

        response = APIClient().put(
            f"/api/cast_members/{actor_cast_member.id}/",
            data={
                "name": "Lana Wachowski",
                "type": "DIRECTOR",
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_cast_member = cast_member_repository.get_by_id(actor_cast_member.id)
        assert updated_cast_member.name == "Lana Wachowski"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_when_cast_member_not_exists_then_return_404(self) -> None:
        response = APIClient().put(
            f"/api/cast_members/{uuid.uuid4()}/",
            data={
                "name": "Lana Wachowski",
                "type": "DIRECTOR",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        response = APIClient().delete("/api/cast_members/123123123/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        response = APIClient().delete(f"/api/cast_members/{uuid.uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_cast_member_exists_then_delete_and_return_204(
        self,
        actor_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(actor_cast_member)

        response = APIClient().delete(f"/api/cast_members/{actor_cast_member.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert cast_member_repository.get_by_id(actor_cast_member.id) is None
        assert cast_member_repository.list() == []
