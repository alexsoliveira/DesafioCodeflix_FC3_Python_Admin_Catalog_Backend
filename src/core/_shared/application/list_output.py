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

def sort_and_paginate(items: list[T], order_by: str, current_page: int, per_page: int = 2) -> ListOutput[T]:
    sorted_items = sorted(items, key=lambda item: getattr(item, order_by))
    page_offset = (current_page - 1) * per_page
    page_items = sorted_items[page_offset:page_offset + per_page]
    
    return ListOutput[T](
        data=page_items,
        meta=ListOutputMeta(
            current_page=current_page,
            per_page=per_page,
            total=len(items)
        )
    )
