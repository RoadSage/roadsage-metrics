from ..database import UserTable
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

    def test_login_no_username(self) -> None:
        response = self.client.post("/login", data={"password": "password"})

        assert response.status_code == 422

    def test_login_no_user(self) -> None:
        response = self.client.post(
            "/login", data={"username": "bob@gmail.com", "password": "password"}
        )

        assert response.status_code == 401

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
            "admin": False,
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

    def test_successful_signup(self) -> None:
        matching_users = (
            UserTable.objects().where(UserTable.email == "alfie@gmail.com").run_sync()
        )
        assert len(matching_users) == 0

        response = self.client.post(
            "/signup",
            json={
                "email": "alfie@gmail.com",
                "password": "password",
                "full_name": "Alfie Wickers",
            },
        )

        assert response.status_code == 200

        body = response.json()
        assert type(body["access_token"]) == str
        assert body["token_type"] == "bearer"

        matching_users = (
            UserTable.objects().where(UserTable.email == "alfie@gmail.com").run_sync()
        )
        assert len(matching_users) == 1

    def test_signup_user_already_exists(self) -> None:
        response = self.client.post(
            "/signup",
            json={
                "email": "sally@gmail.com",
                "password": "password",
                "full_name": "Sara",
            },
        )

        assert response.status_code == 409

        body = response.json()
        assert body == {"detail": "User with email 'sally@gmail.com' already exists"}

    def test_update_password(self) -> None:
        # first login with original password
        response = self.client.post(
            "/login", data={"username": "johndoe@gmail.com", "password": "password"}
        )
        assert response.status_code == 200

        # update password
        response = self.client.put(
            "/users/me/update-password",
            json={"new_password": "new_password"},
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.json() == {"detail": "Password updated successfully"}
        assert response.status_code == 200

        # old password should no longer work
        response = self.client.post(
            "/login", data={"username": "johndoe@gmail.com", "password": "password"}
        )
        assert response.status_code == 401

        # new password should work
        response = self.client.post(
            "/login", data={"username": "johndoe@gmail.com", "password": "new_password"}
        )
        assert response.status_code == 200
