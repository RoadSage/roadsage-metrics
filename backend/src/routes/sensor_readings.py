from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..database import create_sensor_readings, get_sensor_readings_in_range
from ..schemas import Message, SensorReading, User
from ..utils.auth import get_current_active_user

router = APIRouter(tags=["Sensor Readings"], prefix="/sensor-readings")


@router.get("/", response_model=List[SensorReading])
async def get_sensor_readings(
    from_date: date,
    to_date: date,
    user: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> List[SensorReading]:
    """
    Get all sensor readings for the current user, in a specified date range.

    Dates are required and inclusive. If the user is an admin, the user can be specified in the URL.
    """

    if user is not None:
        if current_user.admin:
            return await get_sensor_readings_in_range(user, from_date, to_date)
        else:
            raise HTTPException(
                status_code=403,
                detail="Must be an Admin user to access other users data",
            )

    return await get_sensor_readings_in_range("johndoe@gmail.com", from_date, to_date)


@router.post("/", response_model=Message)
async def add_sensor_readings(
    readings: List[SensorReading], current_user: User = Depends(get_current_active_user)
) -> Message:
    """
    Upload sensor readings to the database.

    There is a limit to the number of reading which can be sent per request. 1000 readings has been tested, and it is recommened to keep batches to a maximum of 1000.
    """

    try:
        await create_sensor_readings(current_user.email, readings)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problem adding sensor reading to the database",
        )

    return Message(detail=f"Successfully added {len(readings)} sensor readings")
