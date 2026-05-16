from rest_framework import serializers

class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())

class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = SetField(
        child=serializers.UUIDField(),
        source="category_ids",
        required=False,
        default=set,
    )

class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
