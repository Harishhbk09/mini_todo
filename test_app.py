"""Automated tests - the CI pipeline runs these on every push."""
import pytest

import app as todo_app


@pytest.fixture
def client():
    todo_app.todos.clear()
    todo_app.next_id = 1
    return todo_app.app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_add_and_list(client):
    r = client.post("/api/todos", json={"title": "Learn Docker"})
    assert r.status_code == 201
    assert client.get("/api/todos").get_json()[0]["title"] == "Learn Docker"


def test_add_requires_title(client):
    assert client.post("/api/todos", json={}).status_code == 400


def test_toggle_and_delete(client):
    client.post("/api/todos", json={"title": "Deploy"})
    assert client.patch("/api/todos/1").get_json()["done"] is True
    assert client.delete("/api/todos/1").status_code == 204
    assert client.delete("/api/todos/1").status_code == 404
