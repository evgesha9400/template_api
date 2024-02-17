"""This module contains query parameter type definitions and validators."""

from typing import List

from fastapi import Query
from typing_extensions import Annotated


ItemIds = Annotated[
    List[int],
    Query(
        title="Item IDs",
        description="The IDs of the items to get",
        min_items=1
    )
]


def validate_item_ids(item_ids: ItemIds) -> ItemIds:
    print("Validating item IDs")
    return item_ids
