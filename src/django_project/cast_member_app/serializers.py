from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super().__init__(
            choices=[member.value for member in CastMemberType],
            **kwargs,
        )

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return CastMemberType(value)

    def to_representation(self, value):
        if isinstance(value, CastMemberType):
            return value.value
        return super().to_representation(value)


class CastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class ListCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(many=True)


class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()


class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()


class DeleteCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
