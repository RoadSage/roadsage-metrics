from logging import disable
from typing import Optional

from piccolo.columns.column_types import Boolean, Secret, Text, Varchar
from piccolo.table import Table

from .schemas import UserInDB


class UserTable(Table):
    email = Text(null=False, primary_key=True)
    hashed_password = Secret()
    full_name = Text()
    disabled = Boolean(default=False)


async def get_user(email: str) -> Optional[UserInDB]:
    user = (
        await UserTable.select(
            UserTable.email,
            UserTable.hashed_password,
            UserTable.full_name,
            UserTable.disabled,
        )
        .where(UserTable.email == email)
        .first()
        .run()
    )

    if not user:
        return None
    return UserInDB(**user)


async def create_user(user: UserInDB) -> None:
    UserTable.insert(
        UserTable(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            disabled=user.disabled,
        )
    ).run()
