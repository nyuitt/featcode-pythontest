import pytest


CATEGORY = {"name": "Notebooks", "description": "Laptops e ultrabooks"}

PRODUCT_PAYLOAD = {
    "name": "MacBook Air M3",
    "description": "Apple M3 16GB 512GB",
    "price": 12499.99,
    "stock": 10,
    "category_id": None,
}


def _create_category(client):
    return client.post("/categories/", json=CATEGORY).json()


def _create_product(client, category_id=None):
    payload = {**PRODUCT_PAYLOAD, "category_id": category_id}
    return client.post("/products/", json=payload).json()


def test_create_product(client):
    cat = _create_category(client)
    payload = {**PRODUCT_PAYLOAD, "category_id": cat["id"]}
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "MacBook Air M3"
    assert float(data["price"]) == 12499.99
    assert data["stock"] == 10
    assert data["category_id"] == cat["id"]


def test_create_product_without_category(client):
    response = client.post("/products/", json=PRODUCT_PAYLOAD)
    assert response.status_code == 201
    assert response.json()["category_id"] is None


def test_list_products_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products(client):
    _create_product(client)
    _create_product(client)
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_products_search(client):
    _create_product(client)
    client.post("/products/", json={**PRODUCT_PAYLOAD, "name": "Dell XPS"})
    response = client.get("/products/?search=mac")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "MacBook" in results[0]["name"]


def test_list_products_filter_by_category(client):
    cat = _create_category(client)
    _create_product(client, category_id=cat["id"])
    _create_product(client)
    response = client.get(f"/products/?category_id={cat['id']}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_products_pagination(client):
    for _ in range(5):
        _create_product(client)
    response = client.get("/products/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product(client):
    created = _create_product(client)
    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_product_not_found(client):
    response = client.get("/products/id-inexistente")
    assert response.status_code == 404


def test_update_product(client):
    created = _create_product(client)
    response = client.patch(f"/products/{created['id']}", json={"price": 9999.00})
    assert response.status_code == 200
    assert float(response.json()["price"]) == 9999.00


def test_update_product_not_found(client):
    response = client.patch("/products/id-inexistente", json={"price": 100})
    assert response.status_code == 404


def test_update_stock(client):
    created = _create_product(client)
    response = client.patch(f"/products/{created['id']}/stock", json={"stock": 50})
    assert response.status_code == 200
    assert response.json()["stock"] == 50


def test_update_stock_not_found(client):
    response = client.patch("/products/id-inexistente/stock", json={"stock": 50})
    assert response.status_code == 404


def test_delete_product(client):
    created = _create_product(client)
    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 204


def test_delete_product_not_found(client):
    response = client.delete("/products/id-inexistente")
    assert response.status_code == 404


def test_low_stock_products(client):
    client.post("/products/", json={**PRODUCT_PAYLOAD, "stock": 5})
    client.post("/products/", json={**PRODUCT_PAYLOAD, "stock": 15})
    response = client.get("/products/low-stock")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["stock"] == 5


def test_low_stock_empty(client):
    client.post("/products/", json={**PRODUCT_PAYLOAD, "stock": 20})
    response = client.get("/products/low-stock")
    assert response.status_code == 200
    assert response.json() == []
