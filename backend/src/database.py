from piccolo.columns.column_types import Boolean, Secret, Text, Varchar
from piccolo.table import Table

from .schemas import UserInDB


class UserTable(Table):
    username = Varchar(40, null=False, primary_key=True)
    hashed_password = Secret()
    email = Text()
    full_name = Text()
    disabled = Boolean(default=False)


async def get_user(username: str) -> UserInDB:
    return UserInDB(
        **await UserTable.select(
            UserTable.username,
            UserTable.hashed_password,
            UserTable.email,
            UserTable.full_name,
            UserTable.disabled,
        )
        .where(UserTable.username == username)
        .first()
        .run()
    )
