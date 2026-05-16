import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.django_project.cast_member_app.models import CastMember as CastMemberModel


@pytest.mark.django_db(transaction=True)
class TestCreateUpdateAndDeleteCastMember:
    def setup_method(self):
        CastMemberModel.objects.all().delete()

    def test_user_can_create_update_and_delete_cast_member(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {"data": []}

        create_response = api_client.post(
            "/api/cast_members/",
            data={
                "name": "Keanu Reeves",
                "type": "ACTOR",
            },
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_cast_member_id = create_response.data["id"]

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": str(created_cast_member_id),
                    "name": "Keanu Reeves",
                    "type": "ACTOR",
                }
            ]
        }

        update_response = api_client.put(
            f"/api/cast_members/{created_cast_member_id}/",
            data={
                "name": "Lana Wachowski",
                "type": "DIRECTOR",
            },
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": str(created_cast_member_id),
                    "name": "Lana Wachowski",
                    "type": "DIRECTOR",
                }
            ]
        }

        delete_response = api_client.delete(
            f"/api/cast_members/{created_cast_member_id}/"
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.data == {"data": []}
