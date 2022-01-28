from typing import List, Optional

from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.column_types import (
    Boolean,
    Float,
    ForeignKey,
    Secret,
    Text,
    Timestamp,
)
from piccolo.table import Table

from .schemas import SensorReading, UserInDB


class UserTable(Table):
    email = Text(null=False, primary_key=True)
    hashed_password = Secret()
    full_name = Text()
    disabled = Boolean(default=False)
    admin = Boolean(default=False)


async def get_user(email: str) -> Optional[UserInDB]:
    user = (
        await UserTable.select(
            UserTable.email,
            UserTable.hashed_password,
            UserTable.full_name,
            UserTable.disabled,
            UserTable.admin,
        )
        .where(UserTable.email == email)
        .first()
        .run()
    )

    if not user:
        return None
    return UserInDB(**user)


async def create_user(user: UserInDB) -> None:
    await UserTable.insert(
        UserTable(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            disabled=user.disabled,
            admin=user.admin,
        )
    ).run()


class SensorReadingTable(Table):
    user = ForeignKey(
        UserTable,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
    )

    timestamp = Timestamp()
    text_displayed = Text(null=True)

    lidar_distance = Float()
    ultrasonic_distance = Float()

    accelerometer_x = Float()
    accelerometer_y = Float()
    accelerometer_z = Float()

    gyroscope_x = Float()
    gyroscope_y = Float()
    gyroscope_z = Float()


async def create_sensor_readings(user: str, readings: List[SensorReading]) -> None:
    await SensorReadingTable.insert(
        *[
            SensorReadingTable(
                user=user,
                timestamp=reading.timestamp,
                text_displayed=reading.text_displayed,
                lidar_distance=reading.lidar_distance,
                ultrasonic_distance=reading.ultrasonic_distance,
                accelerometer_x=reading.accelerometer.x,
                accelerometer_y=reading.accelerometer.y,
                accelerometer_z=reading.accelerometer.z,
                gyroscope_x=reading.gyroscope.x,
                gyroscope_y=reading.gyroscope.y,
                gyroscope_z=reading.gyroscope.z,
            )
            for reading in readings
        ]
    ).run()

    return None
