from logging import disable
from typing import Optional

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

from .schemas import UserInDB


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

