from datetime import date
from typing import Dict, List, Optional

from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.column_types import (
    Boolean,
    Float,
    ForeignKey,
    Secret,
    Text,
    Timestamp,
    Varchar,
)
from piccolo.query.methods.select import Count
from piccolo.table import Table

<<<<<<< HEAD
from .schemas import SensorReading, User, UserInDB
=======
from .schemas import AppCommand, SensorReading, UserInDB
>>>>>>> 6a93221 (feat: add app command api routes)


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


async def update_user_password(user: User, new_password_hash: str) -> None:
    await (
        UserTable.update(hashed_password=new_password_hash)
        .where(UserTable.email == user.email)
        .run()
    )


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


async def get_sensor_readings_in_range(
    user: str, from_date: date, to_date: date
) -> List[SensorReading]:
    return [
        SensorReading.from_database_dictionary(reading)
        for reading in await SensorReadingTable.select(
            SensorReadingTable.timestamp,
            SensorReadingTable.text_displayed,
            SensorReadingTable.lidar_distance,
            SensorReadingTable.ultrasonic_distance,
            SensorReadingTable.accelerometer_x,
            SensorReadingTable.accelerometer_y,
            SensorReadingTable.accelerometer_z,
            SensorReadingTable.gyroscope_x,
            SensorReadingTable.gyroscope_y,
            SensorReadingTable.gyroscope_z,
        )
        .where(SensorReadingTable.user == user)
        .where(SensorReadingTable.timestamp >= from_date)
        .where(SensorReadingTable.timestamp <= to_date)
        .run()
    ]


async def get_message_count(user: str) -> Dict[str, int]:
    counts = (
        await SensorReadingTable.select(
            SensorReadingTable.text_displayed,
            Count(SensorReadingTable.timestamp),
        )
        .group_by(SensorReadingTable.text_displayed)
        .where(SensorReadingTable.user == user)
        .run()
    )

    return {
        result["text_displayed"]: result["count"]
        for result in counts
        if result["text_displayed"] is not None
    }


class AppCommandTable(Table):
    user = ForeignKey(
        UserTable,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
    )

    timestamp = Timestamp()
    command = Text(null=False)
    invocation_method = Varchar(20)


async def get_app_commands_in_range(
    user: str, from_date: date, to_date: date
) -> List[AppCommand]:
    return [
        AppCommand(**reading)
        for reading in await AppCommandTable.select(
            AppCommandTable.timestamp,
            AppCommandTable.command,
            AppCommandTable.invocation_method,
        )
        .where(AppCommandTable.user == user)
        .where(AppCommandTable.timestamp >= from_date)
        .where(AppCommandTable.timestamp <= to_date)
        .run()
    ]


async def add_app_commands(user: str, commands: List[AppCommand]) -> None:
    await AppCommandTable.insert(
        *[
            AppCommandTable(
                user=user,
                timestamp=command.timestamp,
                command=command.command,
                invocation_method=command.invocation_method,
            )
            for command in commands
        ]
    ).run()

    return None
