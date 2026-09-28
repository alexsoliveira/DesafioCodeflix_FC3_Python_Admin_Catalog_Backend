from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 2
    total: int = 0

@dataclass
class ListOutput(Generic[T]):
    data: list[T]
    meta: ListOutputMeta
