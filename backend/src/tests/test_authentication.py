import pytest
from fastapi.testclient import TestClient
from piccolo.engine import engine_finder

from .helpers import TestCase


class TestAuthentication(TestCase):
    def test_successful_login(self) -> None:
        response = self.client.post(
            "/login", data={"username": "johndoe@gmail.com", "password": "password"}
        )

        body = response.json()
        assert type(body["access_token"]) == str
        assert body["token_type"] == "bearer"

        assert response.status_code == 200

    def test_wrong_password(self) -> None:
        response = self.client.post(
            "/login", data={"username": "johndoe@gmail.com", "password": "hello_world"}
        )

        body = response.json()

        assert response.status_code == 401
        assert body == {"detail": "Incorrect email or password"}

    def test_get_current_user_not_logged_in(self) -> None:
        response = self.client.get("/users/me")

        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_current_user_logged_in(self) -> None:
        response = self.client.get(
            "/users/me", headers={"Authorization": f"Bearer {self.get_token()}"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "disabled": False,
            "email": "johndoe@gmail.com",
            "full_name": "Johnathan Doe",
        }

    def test_get_inactive_user(self) -> None:
        response = self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {self.get_token('sally@gmail.com')}"},
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user"}

    def test_bad_jwt(self) -> None:
        response = self.client.get(
            "/users/me", headers={"Authorization": f"Bearer IAmAToken"}
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}
