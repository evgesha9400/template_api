"""This module contains the response models for the API endpoints."""

from pydantic import BaseModel


class CreateItem(BaseModel):
    item_name: str


class UpdateItem(BaseModel):
    item_name: str
