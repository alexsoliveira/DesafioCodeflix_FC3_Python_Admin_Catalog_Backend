import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")

        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")

        if not isinstance(self.type, CastMemberType):
            raise ValueError("type must be a valid CastMemberType")

    def update(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

