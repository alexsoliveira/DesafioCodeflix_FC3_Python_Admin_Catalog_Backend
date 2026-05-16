import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db(transaction=True)
class TestDjangoORMCastMemberRepository:
    def setup_method(self):
        CastMemberModel.objects.all().delete()

    def test_save_cast_member_in_database(self):
        cast_member = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberModel.objects.count() == 1

        cast_member_db = CastMemberModel.objects.get()
        assert cast_member_db.id == cast_member.id
        assert cast_member_db.name == cast_member.name
        assert cast_member_db.type == cast_member.type.value

    def test_get_by_id_returns_domain_entity(self):
        cast_member = CastMemberModel.objects.create(
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR.value,
        )
        repository = DjangoORMCastMemberRepository()

        result = repository.get_by_id(cast_member.id)

        assert result is not None
        assert result.id == cast_member.id
        assert result.name == "Christopher Nolan"
        assert result.type == CastMemberType.DIRECTOR

    def test_list_returns_domain_entities(self):
        actor = CastMemberModel.objects.create(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR.value,
        )
        director = CastMemberModel.objects.create(
            name="Lana Wachowski",
            type=CastMemberType.DIRECTOR.value,
        )
        repository = DjangoORMCastMemberRepository()

        result = repository.list()

        assert len(result) == 2
        assert result[0] == CastMember(
            id=actor.id,
            name=actor.name,
            type=CastMemberType.ACTOR,
        )
        assert result[1] == CastMember(
            id=director.id,
            name=director.name,
            type=CastMemberType.DIRECTOR,
        )

    def test_update_persists_changes(self):
        cast_member = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member)

        cast_member.update(
            name="Lana Wachowski",
            type=CastMemberType.DIRECTOR,
        )
        repository.update(cast_member)

        updated_cast_member = CastMemberModel.objects.get(id=cast_member.id)
        assert updated_cast_member.name == "Lana Wachowski"
        assert updated_cast_member.type == CastMemberType.DIRECTOR.value

    def test_delete_removes_cast_member(self):
        cast_member = CastMember(
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member)

        assert CastMemberModel.objects.filter(id=cast_member.id).exists() is True
        repository.delete(cast_member.id)

        assert CastMemberModel.objects.filter(id=cast_member.id).exists() is False
