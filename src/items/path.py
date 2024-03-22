"""This module contains validators for path parameters."""
from typing import Annotated

from fastapi import Path

ItemId = Annotated[
    int,
    Path(
        default=...,
        title="Item ID",
        description="The ID of the item to get",
        gt=0,
        example=1,
    ),
]
