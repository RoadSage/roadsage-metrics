from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..database import add_app_commands, get_app_commands_in_range
from ..schemas import AppCommand, Message, User
from ..utils.auth import get_current_active_user

router = APIRouter(tags=["App Commands"], prefix="/app-commands")


@router.get("/", response_model=List[AppCommand])
async def get_app_commands_performed(
    from_date: date,
    to_date: date,
    user: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> List[AppCommand]:
    """
    Get all app commands performed by the current user, in a specified date range.

    Dates are required and inclusive. If the user is an admin, the user can be specified in the URL.
    """

    if user is not None:
        if current_user.admin:
            return await get_app_commands_in_range(user, from_date, to_date)
        else:
            raise HTTPException(
                status_code=403,
                detail="Must be an Admin user to access other users data",
            )

    return await get_app_commands_in_range(current_user.email, from_date, to_date)


@router.post("/", response_model=Message)
async def record_app_commands(
    readings: List[AppCommand], current_user: User = Depends(get_current_active_user)
) -> Message:
    """
    Upload app commands to the database.

    There is a limit to the number of reading which can be sent per request. 1000 readings has been tested, and it is recommened to keep batches to a maximum of 1000.
    """

    try:
        await add_app_commands(current_user.email, readings)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problem adding app commands to the database",
        )

    return Message(detail=f"Successfully recorded {len(readings)} app commands")
