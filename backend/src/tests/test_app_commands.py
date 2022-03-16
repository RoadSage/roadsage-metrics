import datetime
from typing import Dict, Union

from ..database import AppCommandTable
from .helpers import TestCase

sample_app_command = {
    "timestamp": "2020-01-01T00:00:00.000Z",
    "command": "Hello World",
    "invocation_method": "touch",
}

malformed_app_command = {
    "timestamp": "2020-01-01T00:00:00.000Z",
    "command": "Hello World",
    "invocation_method": "unknown::method",
}


class TestAddAppCommands(TestCase):
    def test_not_authenticated(self) -> None:
        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer IAmAToken"},
            json=[sample_app_command],
        )
        print(response.json())
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

    def test_malformed_app_command(self) -> None:
        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[malformed_app_command],
        )

        assert response.status_code == 422

    def test_one_app_command(self) -> None:
        previous_number_of_app_commands = len(AppCommandTable.select().run_sync())
        hello_world_reading = (
            AppCommandTable.select(
                AppCommandTable.invocation_method, AppCommandTable.timestamp
            )
            .where(AppCommandTable.command == "Hello World")
            .first()
            .run_sync()
        )
        assert hello_world_reading == None

        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[sample_app_command],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully recorded 1 app commands"}

        number_of_app_commands = len(AppCommandTable.select().run_sync())
        assert number_of_app_commands == previous_number_of_app_commands + 1

        hello_world_reading = (
            AppCommandTable.select(
                AppCommandTable.invocation_method, AppCommandTable.timestamp
            )
            .where(AppCommandTable.command == "Hello World")
            .first()
            .run_sync()
        )
        assert hello_world_reading["invocation_method"] == "touch"
        assert hello_world_reading["timestamp"] == datetime.datetime(
            2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
        )

    def test_hundred_app_commands(self) -> None:
        previous_number_of_app_commands = len(AppCommandTable.select().run_sync())

        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "command": "Hello World" if i % 10 == 0 else "Sorry",
                    "invocation_method": "touch" if i % 3 == 0 else "voice",
                }
                for i in range(100)
            ],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully recorded 100 app commands"}

        number_of_app_commands = len(AppCommandTable.select().run_sync())
        assert number_of_app_commands == previous_number_of_app_commands + 100

    def test_thousand_app_commands(self) -> None:
        previous_number_of_app_commands = len(AppCommandTable.select().run_sync())

        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "command": "Hello World" if i % 10 == 0 else "Sorry",
                    "invocation_method": "touch" if i % 3 == 0 else "voice",
                }
                for i in range(1000)
            ],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully recorded 1000 app commands"}

        number_of_app_commands = len(AppCommandTable.select().run_sync())
        assert number_of_app_commands == previous_number_of_app_commands + 1000

    def test_too_many_commands_for_the_database(self) -> None:
        previous_number_of_app_commands = len(AppCommandTable.select().run_sync())

        response = self.client.post(
            "/app-commands/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "command": "Hello World" if i % 10 == 0 else "Sorry",
                    "invocation_method": "touch" if i % 3 == 0 else "voice",
                }
                for i in range(100000)
            ],
        )

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Problem adding app commands to the database"
        }

        number_of_app_commands = len(AppCommandTable.select().run_sync())
        assert number_of_app_commands == previous_number_of_app_commands


class TestGetAppCommands(TestCase):
    def test_get_between_dates(self) -> None:
        response = self.client.get(
            "/app-commands/?from_date=2019-12-31&to_date=2021-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.status_code == 200
        assert response.json() == [
            {
                "command": "Too Close",
                "invocation_method": "touch",
                "timestamp": "2020-01-01T12:00:00",
            },
            {
                "command": "Thanks!",
                "invocation_method": "voice",
                "timestamp": "2020-01-03T14:04:00",
            },
            {
                "command": "Sorry",
                "invocation_method": "voice",
                "timestamp": "2020-05-07T14:09:01",
            },
        ]

    def test_no_commands_in_range(self) -> None:
        response = self.client.get(
            "/app-commands/?from_date=2020-12-31&to_date=2022-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_access_other_user_not_admin(self) -> None:
        response = self.client.get(
            "/app-commands/?user=bob&from_date=2019-12-31&to_date=2020-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.json() == {
            "detail": "Must be an Admin user to access other users data"
        }
        assert response.status_code == 403

    def test_access_other_user_admin(self) -> None:
        response = self.client.get(
            "/app-commands/?user=sally@gmail.com&from_date=2019-12-31&to_date=2020-01-03",
            headers={"Authorization": f"Bearer {self.get_token('admin@gmail.com')}"},
        )

        assert response.status_code == 200
        assert response.json() == [
            {
                "command": "Thanks!",
                "invocation_method": "voice",
                "timestamp": "2020-01-01T12:00:00",
            },
            {
                "command": "Sorry",
                "invocation_method": "voice",
                "timestamp": "2020-01-01T13:00:00",
            },
        ]
