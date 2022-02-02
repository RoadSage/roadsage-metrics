import os
from datetime import datetime
from typing import Callable

from fastapi.testclient import TestClient
from piccolo.engine import engine_finder

from ..database import SensorReadingTable, UserTable
from ..main import app
from ..utils.auth import get_password_hash


def create_tables() -> None:
    UserTable.create_table(if_not_exists=True).run_sync()
    SensorReadingTable.create_table(if_not_exists=True).run_sync()


def add_sample_data() -> None:
    # Clear exisiting data
    UserTable.delete(force=True).run_sync()
    SensorReadingTable.delete(force=True).run_sync()

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
        UserTable(
            hashed_password=get_password_hash("password"),
            email="admin@gmail.com",
            full_name="Admin Account",
            disabled=False,
            admin=True,
        ),
    ).run_sync()

    SensorReadingTable.insert(
        SensorReadingTable(
            user="johndoe@gmail.com",
            timestamp=datetime(2020, 1, 1, 12, 0, 0),
            text_displayed="Thanks!",
            lidar_distance=11.0,
            ultrasonic_distance=10.0,
            accelerometer_x=7.0,
            accelerometer_y=8.0,
            accelerometer_z=9.0,
            gyroscope_x=4.0,
            gyroscope_y=5.0,
            gyroscope_z=6.0,
        ),
        SensorReadingTable(
            user="johndoe@gmail.com",
            timestamp=datetime(2020, 1, 1, 12, 0, 1),
            text_displayed=None,
            lidar_distance=10.0,
            ultrasonic_distance=18.0,
            accelerometer_x=7.0,
            accelerometer_y=8.5,
            accelerometer_z=9.0,
            gyroscope_x=4.0,
            gyroscope_y=5.0,
            gyroscope_z=6.3,
        ),
        SensorReadingTable(
            user="johndoe@gmail.com",
            timestamp=datetime(2020, 1, 4, 16, 0, 1),
            text_displayed=None,
            lidar_distance=15.0,
            ultrasonic_distance=18.3,
            accelerometer_x=7.0,
            accelerometer_y=8.5,
            accelerometer_z=9.1,
            gyroscope_x=4.0,
            gyroscope_y=5.0,
            gyroscope_z=6.3,
        ),
        SensorReadingTable(
            user="sally@gmail.com",
            timestamp=datetime(2020, 1, 1, 12, 0, 0),
            text_displayed="Sorry",
            lidar_distance=11.0,
            ultrasonic_distance=10.0,
            accelerometer_x=7.0,
            accelerometer_y=8.0,
            accelerometer_z=9.0,
            gyroscope_x=4.0,
            gyroscope_y=5.0,
            gyroscope_z=6.0,
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
