import uuid

from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.cast_member_app.serializers import (
    CastMemberResponseSerializer,
    CreateCastMemberRequestSerializer,
    UpdateCastMemberRequestSerializer,
)


class TestCreateCastMemberRequestSerializer:
    def test_serializer_accepts_actor_and_converts_to_enum(self):
        serializer = CreateCastMemberRequestSerializer(
            data={
                "name": "Keanu Reeves",
                "type": "ACTOR",
            }
        )

        assert serializer.is_valid() is True
        assert serializer.validated_data["name"] == "Keanu Reeves"
        assert serializer.validated_data["type"] == CastMemberType.ACTOR

    def test_serializer_accepts_director_and_converts_to_enum(self):
        serializer = CreateCastMemberRequestSerializer(
            data={
                "name": "Christopher Nolan",
                "type": "DIRECTOR",
            }
        )

        assert serializer.is_valid() is True
        assert serializer.validated_data["type"] == CastMemberType.DIRECTOR

    def test_serializer_rejects_invalid_type(self):
        serializer = CreateCastMemberRequestSerializer(
            data={
                "name": "Keanu Reeves",
                "type": "WRITER",
            }
        )

        assert serializer.is_valid() is False
        assert "type" in serializer.errors

    def test_serializer_rejects_blank_name(self):
        serializer = CreateCastMemberRequestSerializer(
            data={
                "name": "",
                "type": "ACTOR",
            }
        )

        assert serializer.is_valid() is False
        assert "name" in serializer.errors


class TestUpdateCastMemberRequestSerializer:
    def test_serializer_accepts_valid_payload(self):
        serializer = UpdateCastMemberRequestSerializer(
            data={
                "id": str(uuid.uuid4()),
                "name": "Lana Wachowski",
                "type": "DIRECTOR",
            }
        )

        assert serializer.is_valid() is True
        assert serializer.validated_data["type"] == CastMemberType.DIRECTOR


class TestCastMemberResponseSerializer:
    def test_serializer_converts_enum_to_string(self):
        serializer = CastMemberResponseSerializer(
            instance={
                "id": uuid.uuid4(),
                "name": "Keanu Reeves",
                "type": CastMemberType.ACTOR,
            }
        )

        assert serializer.data["type"] == "ACTOR"
