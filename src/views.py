from fastapi import Depends

from main import app
import requests as req
import responses as res
import path
import query


@app.get(
    path="/items/{item_id}",
    response_model=res.GetItem,
 )
async def get_item(
    item_id: int = Depends(path.validate_item_id),
):
    return res.GetItem(item_id=item_id, item_name="Item 1")


@app.get(
    path="/items",
    response_model=res.GetItems,
)
async def get_items(
    item_ids: query.ItemIds = Depends(query.validate_item_ids),
):
    items = []
    for item_id in item_ids:
        items.append(res.GetItem(item_id=item_id, item_name=f"Item {item_id}"))
    return res.GetItems(items=items)


@app.post("/items")
async def create_item(
    item: req.CreateItem,
):
    return res.CreateItem(item_id=1, item_name=item.item_name)


@app.put("/items/{item_id}")
async def update_item(
    item: req.UpdateItem,
    item_id: int = Depends(path.validate_item_id),
):
    return res.UpdateItem(item_id=item_id, item_name=item.item_name)


@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int = Depends(path.validate_item_id),
):
    return res.DeleteItem(item_id=item_id, item_name=f"Item {item_id}")
