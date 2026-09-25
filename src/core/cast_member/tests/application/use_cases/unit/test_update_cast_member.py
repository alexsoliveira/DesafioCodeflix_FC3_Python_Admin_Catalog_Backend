import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberRequest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_name(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Lana Wachowski",
        )

        use_case.execute(request)

        assert cast_member.name == "Lana Wachowski"
        assert cast_member.type == CastMemberType.ACTOR
        mock_repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_type(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            type=CastMemberType.DIRECTOR,
        )

        use_case.execute(request)

        assert cast_member.name == "Keanu Reeves"
        assert cast_member.type == CastMemberType.DIRECTOR
        mock_repository.update.assert_called_once_with(cast_member)

    def test_when_cast_member_does_not_exist_should_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCastMember(repository=mock_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(
                UpdateCastMemberRequest(
                    id=uuid.uuid4(),
                    name="Lana Wachowski",
                )
            )

        mock_repository.update.assert_not_called()

    def test_update_cast_member_with_invalid_data(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Keanu Reeves",
            type=CastMemberType.ACTOR,
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)

        with pytest.raises(InvalidCastMemberData, match="name cannot be empty") as exc_info:
            use_case.execute(
                UpdateCastMemberRequest(
                    id=cast_member.id,
                    name="",
                )
            )

        assert exc_info.type is InvalidCastMemberData
        assert str(exc_info.value) == "name cannot be empty"
        mock_repository.update.assert_not_called()
