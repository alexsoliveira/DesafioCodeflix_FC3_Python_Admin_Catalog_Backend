from uuid import uuid4

from django.db import models

from src.core.cast_member.domain.cast_member import CastMemberType


class CastMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=[(member.value, member.value) for member in CastMemberType],
    )

    class Meta:
        db_table = "cast_member"
        app_label = "cast_member_app"

    def __str__(self):
        return self.name
