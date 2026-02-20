CATEGORY = {"name": "Eletrônicos", "description": "Gadgets"}
PRODUCT_BASE = {"name": "Produto Teste", "description": "Desc", "price": 100.0, "stock": 5, "category_id": None}


def test_dashboard_empty(client):
    response = client.get("/dashboard/")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] == 0
    assert data["total_categories"] == 0
    assert float(data["total_stock_value"]) == 0.0
    assert data["low_stock_count"] == 0
    assert data["low_stock_products"] == []
    assert data["products_by_category"] == []


def test_dashboard_with_data(client):
    cat = client.post("/categories/", json=CATEGORY).json()
    client.post("/products/", json={**PRODUCT_BASE, "category_id": cat["id"], "price": 200.0, "stock": 3})
    client.post("/products/", json={**PRODUCT_BASE, "category_id": cat["id"], "price": 100.0, "stock": 15})

    response = client.get("/dashboard/")
    assert response.status_code == 200
    data = response.json()

    assert data["total_products"] == 2
    assert data["total_categories"] == 1
    assert float(data["total_stock_value"]) == (200.0 * 3) + (100.0 * 15)
    assert data["low_stock_count"] == 1
    assert len(data["low_stock_products"]) == 1
    assert len(data["products_by_category"]) == 1
    assert data["products_by_category"][0]["product_count"] == 2


def test_dashboard_total_categories_independent_of_products(client):
    client.post("/categories/", json=CATEGORY)
    client.post("/categories/", json={"name": "Periféricos", "description": "X"})

    response = client.get("/dashboard/")
    data = response.json()
    assert data["total_categories"] == 2
    assert data["total_products"] == 0
