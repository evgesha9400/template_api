from fastapi import APIRouter
from . import path, query
from . import requests as req
from . import responses as res


items = APIRouter(tags=["Items"])


@items.get(
    path="/items/{item_id}",
    response_model=res.GetItem,
)
async def get_item(
    item_id: path.ItemId,
):
    return res.GetItem(item_id=item_id, item_name="Item 1")


@items.get(
    path="/items",
    response_model=res.GetItems,
)
async def get_items(
    item_ids: query.ItemIds = None,
):
    items = []
    for item_id in item_ids:
        items.append(res.GetItem(item_id=item_id, item_name=f"Item {item_id}"))
    return res.GetItems(items=items)


@items.post(
    path="/items",
    response_model=res.CreateItem,
)
async def create_item(
    item: req.CreateItem,
):
    return res.CreateItem(item_id=1, item_name=item.item_name)


@items.put(
    path="/items/{item_id}",
    response_model=res.UpdateItem,
)
async def update_item(
    item: req.UpdateItem,
    item_id: path.ItemId,
):
    return res.UpdateItem(item_id=item_id, item_name=item.item_name)


@items.delete(
    path="/items/{item_id}",
    response_model=res.DeleteItem,
)
async def delete_item(
    item_id: int = path.ItemId,
):
    return res.DeleteItem(item_id=item_id, item_name=f"Item {item_id}")
