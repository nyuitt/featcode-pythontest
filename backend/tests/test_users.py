USER_PAYLOAD = {"full_name": "João Silva", "email": "joao@example.com", "keycloak_id": "kc-001"}


def test_create_user(client):
    response = client.post("/users/", json=USER_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@example.com"
    assert data["full_name"] == "João Silva"
    assert "id" in data


def test_create_user_duplicate_email(client):
    client.post("/users/", json=USER_PAYLOAD)
    response = client.post("/users/", json=USER_PAYLOAD)
    assert response.status_code == 409


def test_list_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_users(client):
    client.post("/users/", json=USER_PAYLOAD)
    response = client.get("/users/")
    assert len(response.json()) == 1


def test_get_user(client):
    created = client.post("/users/", json=USER_PAYLOAD).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_user_not_found(client):
    response = client.get("/users/id-inexistente")
    assert response.status_code == 404


def test_update_user(client):
    created = client.post("/users/", json=USER_PAYLOAD).json()
    response = client.patch(f"/users/{created['id']}", json={"full_name": "João Atualizado"})
    assert response.status_code == 200
    assert response.json()["full_name"] == "João Atualizado"


def test_update_user_not_found(client):
    response = client.patch("/users/id-inexistente", json={"full_name": "Novo Nome"})
    assert response.status_code == 404


def test_delete_user(client):
    created = client.post("/users/", json=USER_PAYLOAD).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 204


def test_delete_user_not_found(client):
    response = client.delete("/users/id-inexistente")
    assert response.status_code == 404
