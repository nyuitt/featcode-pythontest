import pytest


CATEGORY_PAYLOAD = {"name": "Eletrônicos", "description": "Gadgets e dispositivos"}


def test_create_category(client):
    response = client.post("/categories/", json=CATEGORY_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Eletrônicos"
    assert "id" in data


def test_create_category_duplicate(client):
    client.post("/categories/", json=CATEGORY_PAYLOAD)
    response = client.post("/categories/", json=CATEGORY_PAYLOAD)
    assert response.status_code == 409


def test_list_categories_empty(client):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_categories(client):
    client.post("/categories/", json=CATEGORY_PAYLOAD)
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_category(client):
    created = client.post("/categories/", json=CATEGORY_PAYLOAD).json()
    response = client.get(f"/categories/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_category_not_found(client):
    response = client.get("/categories/id-inexistente")
    assert response.status_code == 404


def test_update_category(client):
    created = client.post("/categories/", json=CATEGORY_PAYLOAD).json()
    response = client.patch(f"/categories/{created['id']}", json={"name": "Periféricos Atualizados"})
    assert response.status_code == 200
    assert response.json()["name"] == "Periféricos Atualizados"


def test_update_category_not_found(client):
    response = client.patch("/categories/id-inexistente", json={"name": "Nome Válido"})
    assert response.status_code == 404


def test_delete_category(client):
    created = client.post("/categories/", json=CATEGORY_PAYLOAD).json()
    response = client.delete(f"/categories/{created['id']}")
    assert response.status_code == 204


def test_delete_category_not_found(client):
    response = client.delete("/categories/id-inexistente")
    assert response.status_code == 404
