import os
from typing import Callable

from fastapi.testclient import TestClient
from piccolo.engine import engine_finder

from ..database import UserTable
from ..main import app
from ..utils.auth import get_password_hash


def create_tables() -> None:
    tables = [UserTable]

    for table in tables:
        table.create_table(if_not_exists=True).run_sync()


def add_sample_data() -> None:
    # Clear exisiting data
    UserTable.delete(force=True).run_sync()

    # Add sample data
    UserTable.insert(
        UserTable(
            hashed_password=get_password_hash("password"),
            email="johndoe@gmail.com",
            full_name="Johnathan Doe",
            disabled=False,
        ),
        UserTable(
            hashed_password=get_password_hash("password"),
            email="sally@gmail.com",
            full_name="Sally Smith",
            disabled=True,
        ),
    ).run_sync()


class TestCase:
    def setup_method(self, _test_method: Callable[[], None]) -> None:
        os.environ["APP_SECRET_KEY"] = "secret"
        create_tables()
        add_sample_data()
        self.client = TestClient(app)

    def teardown_method(self, _test_method: Callable[[], None]) -> None:
        engine_finder().remove_db_file()  # type: ignore

    def get_token(self, email: str = "johndoe@gmail.com") -> str:
        response = self.client.post(
            "/login",
            data={"username": email, "password": "password"},
        )

        body = response.json()
        return str(body["access_token"])
