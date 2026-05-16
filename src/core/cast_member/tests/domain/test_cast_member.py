import uuid
from uuid import UUID

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 2 required positional arguments: 'name' and 'type'"):
            CastMember()

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            CastMember(name="a" * 256, type=CastMemberType.ACTOR)

    def test_type_must_be_a_valid_cast_member_type(self):
        with pytest.raises(ValueError, match="type must be a valid CastMemberType"):
            CastMember(name="Keanu Reeves", type="ACTOR")

    def test_created_cast_member_with_default_values(self):
        cast_member = CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)

        assert cast_member.name == "Keanu Reeves"
        assert cast_member.type == CastMemberType.ACTOR
        assert isinstance(cast_member.id, UUID)

    @pytest.mark.parametrize("cast_member_type", [CastMemberType.ACTOR, CastMemberType.DIRECTOR])
    def test_create_cast_member_with_allowed_types(self, cast_member_type):
        cast_member = CastMember(name="Valid Name", type=cast_member_type)
        assert cast_member.type == cast_member_type

    def test_create_cast_member_with_provided_values(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.id == cast_member_id
        assert cast_member.name == "Christopher Nolan"
        assert cast_member.type == CastMemberType.DIRECTOR


class TestEquality:
    def test_when_cast_members_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        cast_member_1 = CastMember(
            id=common_id,
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        cast_member_2 = CastMember(
            id=common_id,
            name="Christopher Nolan",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member_1 == cast_member_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        cast_member = CastMember(
            id=common_id,
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        dummy = Dummy()
        dummy.id = common_id

        assert cast_member != dummy


class TestUpdateCastMember:
    def test_update_cast_member(self):
        cast_member = CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)

        cast_member.update(
            name="Lana Wachowski",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.name == "Lana Wachowski"
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_with_invalid_name(self):
        cast_member = CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.update(name="", type=CastMemberType.DIRECTOR)

    def test_update_cast_member_with_invalid_type(self):
        cast_member = CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="type must be a valid CastMemberType"):
            cast_member.update(name="Lana Wachowski", type="DIRECTOR")
