from tests.conftest import client


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


async def test_user_list():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_login():
    response = client.post(
        "/users/login",
        json={
            "username": "ciccio",
            "password": "ciccio123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password():
    response = client.post(
        "/users/login",
        json={
            "username": "ciccio",
            "password": "sbagliata"
        }
    )
    assert response.status_code == 401
