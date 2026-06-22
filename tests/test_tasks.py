from fastapi.testclient import TestClient
from application.main import app
client = TestClient(app)
def get_auth_headers():
    client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": "test@mail.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
def test_create_task():
    headers = get_auth_headers()
    response = client.post("/todos",
        json={"title": "My task", "description": "description"},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "My task"
def test_get_my_tasks():
    headers = get_auth_headers()
    client.post("/todos",
        json={"title": "My task", "description": "desc"},
        headers=headers
    )
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
def test_delete_task():
    headers = get_auth_headers()
    create = client.post("/todos",
        json={"title": "To delete", "description": "desc"},
        headers=headers
    )
    todo_id = create.json()["id"]
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 204
def test_delete_other_user_task():
    client.post("/auth/register", json={
        "email": "user1@mail.com", "password": "testpass123"
    })
    r = client.post("/auth/login", data={
        "username": "user1@mail.com", "password": "testpass123"
    })
    headers1 = {"Authorization": f"Bearer {r.json()['access_token']}"}
    create = client.post("/todos",
        json={"title": "User1 task"},
        headers=headers1
    )
    todo_id = create.json()["id"]
    client.post("/auth/register", json={
        "email": "user2@mail.com", "password": "testpass123"
    })
    r2 = client.post("/auth/login", data={
        "username": "user2@mail.com", "password": "testpass123"
    })
    headers2 = {"Authorization": f"Bearer {r2.json()['access_token']}"}
    response = client.delete(f"/todos/{todo_id}", headers=headers2)
    assert response.status_code == 403