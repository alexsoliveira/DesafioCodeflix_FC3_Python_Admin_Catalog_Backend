from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberORM = CastMemberORM):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type.value,
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member = self.cast_member_model.objects.get(id=id)
        except self.cast_member_model.DoesNotExist:
            return None

        return CastMember(
            id=cast_member.id,
            name=cast_member.name,
            type=CastMemberType(cast_member.type),
        )

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type.value,
        )

    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType(cast_member.type),
            )
            for cast_member in self.cast_member_model.objects.all()
        ]
