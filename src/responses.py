"""This module contains the response models for the API endpoints."""

from typing import List
from pydantic import BaseModel


class GetItem(BaseModel):
    item_id: int
    item_name: str


class GetItems(BaseModel):
    items: List[GetItem]


class CreateItem(BaseModel):
    item_id: int
    item_name: str


class UpdateItem(BaseModel):
    item_id: int
    item_name: str


class DeleteItem(BaseModel):
    item_id: int
    item_name: str
