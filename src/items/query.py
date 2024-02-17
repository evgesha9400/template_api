"""This module contains query parameter type definitions and validators."""
from typing import List, Union

from fastapi import Query
from pydantic import BeforeValidator
from typing_extensions import Annotated


def string_to_list(item_ids: List[str]) -> Union[List[int], List[str]]:
    """Convert a comma-separated string to a list of integers. When a string is passed as a query parameter,
    it is cast into a List[str] because FastAPI coerces based on declared type."""
    if isinstance(item_ids, List) and len(item_ids) == 1 and "," in item_ids[0]:
        validated_item_ids = [int(item_id) for item_id in item_ids[0].split(",")]
        return validated_item_ids
    return item_ids


ItemIds = Annotated[
    List[int],
    Query(
        title="Item IDs",
        description="The IDs of the items to get",
        required=False,
        example="item_ids=1,2,3 OR item_ids=1&item_ids=2&item_ids=3",
    ),
    BeforeValidator(string_to_list),
]
