from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "item_name": "Item 1"}


def test_get_items():
    response = client.get("/items?item_ids=1,2")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"item_id": 1, "item_name": "Item 1"},
            {"item_id": 2, "item_name": "Item 2"},
        ]
    }


def test_create_item():
    response = client.post("/items", json={"item_name": "New Item"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "item_name": "New Item"}


def test_update_item():
    response = client.put("/items/1", json={"item_name": "Updated Item"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "item_name": "Updated Item"}


def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "item_name": "Item 1"}
