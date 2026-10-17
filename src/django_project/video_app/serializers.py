from rest_framework import serializers

from src.core.video.domain.value_objects import Rating


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))


class RatingField(serializers.ChoiceField):
    """Accepts the Rating name (e.g. "L", "AGE_10") and converts it to the domain enum."""

    def __init__(self, **kwargs):
        super().__init__(choices=[rating.name for rating in Rating], **kwargs)

    def to_internal_value(self, data):
        return Rating[super().to_internal_value(data)]

    def to_representation(self, value):
        return value.name if isinstance(value, Rating) else value


class CreateVideoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    year_launched = serializers.IntegerField(source="launch_year")
    opened = serializers.BooleanField(default=False)
    rating = RatingField()
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    categories_id = SetField(child=serializers.UUIDField(), source="categories", required=False, default=set)
    genres_id = SetField(child=serializers.UUIDField(), source="genres", required=False, default=set)
    cast_members_id = SetField(child=serializers.UUIDField(), source="cast_members", required=False, default=set)


class CreateVideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
