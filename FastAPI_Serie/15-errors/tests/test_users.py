import pytest

from tests.conftest import client


@pytest.fixture(scope="session")
async def test_create_user(ac):
    response = await ac.post(
        "/users/",
        json={
            "username": "ciccio",
            "email": "user@example.com",
            "password": "ciccio123",
            "is_admin": False
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "ciccio"
    assert response.json()["is_admin"] is False
    return response.json()


async def test_user_list(test_create_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == test_create_user["username"]


@pytest.fixture(scope="session")
async def test_login(test_create_user):
    response = client.post(
        "/users/login",
        json={
            "username": "ciccio",
            "password": "ciccio123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]


async def test_login_wrong_password():
    response = client.post(
        "/users/login",
        json={
            "username": "ciccio",
            "password": "sbagliata"
        }
    )
    assert response.status_code == 401


async def test_me(test_login):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {test_login}"})
    assert response.status_code == 200
    assert response.json()["username"] == "ciccio"
