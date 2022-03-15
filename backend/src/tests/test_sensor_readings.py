import datetime
from typing import Dict, Union

from ..database import SensorReadingTable
from .helpers import TestCase

sample_sensor_reading = {
    "timestamp": "2020-01-01T00:00:00.000Z",
    "text_displayed": "Hello World",
    "lidar_distance": 7.0,
    "ultrasonic_distance": 5.0,
    "accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0},
    "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
}

malformed_sensor_reading = {
    "timestamp": "2020-01-01T00:00:00.000Z",
    "text_displayed": None,
    "lidar_distance": 7.0,
    "ultrasonic": 5.0,
    "accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0},
    "gyroscope": {"x": 4.0, "t": 5.0, "z": 6.0},
}


class TestAddSensorReadings(TestCase):
    def test_not_authenticated(self) -> None:
        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer IAmAToken"},
            json=[sample_sensor_reading],
        )
        print(response.json())
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

    def test_malformed_sensor_reading(self) -> None:
        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[malformed_sensor_reading],
        )

        assert response.status_code == 422

    def test_one_sensor_reading(self) -> None:
        previous_number_of_sensor_readings = len(SensorReadingTable.select().run_sync())
        hello_world_reading = (
            SensorReadingTable.select(
                SensorReadingTable.ultrasonic_distance,
                SensorReadingTable.accelerometer_x,
                SensorReadingTable.timestamp,
            )
            .where(SensorReadingTable.text_displayed == "Hello World")
            .first()
            .run_sync()
        )
        assert hello_world_reading == None

        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[sample_sensor_reading],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully added 1 sensor readings"}

        number_of_sensor_readings = len(SensorReadingTable.select().run_sync())
        assert number_of_sensor_readings == previous_number_of_sensor_readings + 1

        hello_world_reading = (
            SensorReadingTable.select(
                SensorReadingTable.ultrasonic_distance,
                SensorReadingTable.accelerometer_x,
                SensorReadingTable.timestamp,
            )
            .where(SensorReadingTable.text_displayed == "Hello World")
            .first()
            .run_sync()
        )
        assert hello_world_reading["ultrasonic_distance"] == 5.0
        assert hello_world_reading["accelerometer_x"] == 1.0
        assert hello_world_reading["timestamp"] == datetime.datetime(
            2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
        )

    def test_hundred_sensor_readings(self) -> None:
        previous_number_of_sensor_readings = len(SensorReadingTable.select().run_sync())

        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "text_displayed": "Hello World" if i % 10 == 0 else None,
                    "lidar_distance": (i * 5 + i) % 21,
                    "ultrasonic_distance": (i * 7 + i) % 20,
                    "accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0},
                    "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
                }
                for i in range(100)
            ],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully added 100 sensor readings"}

        number_of_sensor_readings = len(SensorReadingTable.select().run_sync())
        assert number_of_sensor_readings == previous_number_of_sensor_readings + 100

    def test_thousand_sensor_readings(self) -> None:
        previous_number_of_sensor_readings = len(SensorReadingTable.select().run_sync())

        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "text_displayed": "Hello World" if i % 10 == 0 else None,
                    "lidar_distance": (i * 5 + i) % 21,
                    "ultrasonic_distance": (i * 7 + i) % 20,
                    "accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0},
                    "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
                }
                for i in range(1000)
            ],
        )

        assert response.status_code == 200
        assert response.json() == {"detail": "Successfully added 1000 sensor readings"}

        number_of_sensor_readings = len(SensorReadingTable.select().run_sync())
        assert number_of_sensor_readings == previous_number_of_sensor_readings + 1000

    def test_too_many_readings_for_the_database(self) -> None:
        previous_number_of_sensor_readings = len(SensorReadingTable.select().run_sync())

        response = self.client.post(
            "/sensor-readings/",
            headers={"Authorization": f"Bearer {self.get_token()}"},
            json=[
                {
                    "timestamp": str(
                        datetime.datetime(2020, 1, 1, 1, (i // 60) % 60, i % 60)
                    ),
                    "text_displayed": "Hello World" if i % 10 == 0 else None,
                    "lidar_distance": (i * 5 + i) % 21,
                    "ultrasonic_distance": (i * 7 + i) % 20,
                    "accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0},
                    "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
                }
                for i in range(100000)
            ],
        )

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Problem adding sensor reading to the database"
        }

        number_of_sensor_readings = len(SensorReadingTable.select().run_sync())
        assert number_of_sensor_readings == previous_number_of_sensor_readings


class TestGetSensorReadings(TestCase):
    def test_get_between_dates(self) -> None:
        response = self.client.get(
            "/sensor-readings/?from_date=2019-12-31&to_date=2020-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.status_code == 200
        assert response.json() == [
            {
                "timestamp": "2020-01-01T12:00:00",
                "text_displayed": "Thanks!",
                "lidar_distance": 11.0,
                "ultrasonic_distance": 10.0,
                "accelerometer": {"x": 7.0, "y": 8.0, "z": 9.0},
                "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
            },
            {
                "timestamp": "2020-01-01T12:00:01",
                "text_displayed": None,
                "lidar_distance": 10.0,
                "ultrasonic_distance": 18.0,
                "accelerometer": {"x": 7.0, "y": 8.5, "z": 9.0},
                "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.3},
            },
        ]

    def test_no_events_in_range(self) -> None:
        response = self.client.get(
            "/sensor-readings/?from_date=2020-12-31&to_date=2022-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_access_other_user_not_admin(self) -> None:
        response = self.client.get(
            "/sensor-readings/?user=bob&from_date=2019-12-31&to_date=2020-01-03",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.json() == {
            "detail": "Must be an Admin user to access other users data"
        }
        assert response.status_code == 403

    def test_access_other_user_admin(self) -> None:
        response = self.client.get(
            "/sensor-readings/?user=sally@gmail.com&from_date=2019-12-31&to_date=2020-01-03",
            headers={"Authorization": f"Bearer {self.get_token('admin@gmail.com')}"},
        )

        assert response.status_code == 200
        assert response.json() == [
            {
                "timestamp": "2020-01-01T12:00:00",
                "text_displayed": "Sorry",
                "lidar_distance": 11.0,
                "ultrasonic_distance": 10.0,
                "accelerometer": {"x": 7.0, "y": 8.0, "z": 9.0},
                "gyroscope": {"x": 4.0, "y": 5.0, "z": 6.0},
            }
        ]


class TestGetMessageCounts(TestCase):
    def test_get_message_counts(self) -> None:
        response = self.client.get(
            "/sensor-readings/messages",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.status_code == 200
        assert response.json() == {"Thanks!": 1}

    def test_access_other_user_not_admin(self) -> None:
        response = self.client.get(
            "/sensor-readings/messages?user=bob",
            headers={"Authorization": f"Bearer {self.get_token()}"},
        )

        assert response.json() == {
            "detail": "Must be an Admin user to access other users data"
        }
        assert response.status_code == 403

    def test_access_other_user_admin(self) -> None:
        response = self.client.get(
            "/sensor-readings/messages?user=sally@gmail.com",
            headers={"Authorization": f"Bearer {self.get_token('admin@gmail.com')}"},
        )

        assert response.status_code == 200
        assert response.json() == {"Sorry": 1}
