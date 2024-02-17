"""This module contains validators for path parameters."""

from fastapi import HTTPException


def validate_item_id(item_id: int) -> int:
    if item_id <= 0:
        raise HTTPException(
            status_code=400, detail="Item ID must be a positive integer"
        )
    return item_id
