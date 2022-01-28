from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    email: str
    full_name: str
    disabled: bool = False
    admin: bool = False


class UserInDB(User):
    hashed_password: str


class NewUser(User):
    password: str


class AccelerometerReading(BaseModel):
    x: float
    y: float
    z: float


class GyroscopeReading(BaseModel):
    x: float
    y: float
    z: float


class SensorReading(BaseModel):
    timestamp: datetime
    text_displayed: Optional[str] = None

    lidar_distance: float
    ultrasonic_distance: float

    accelerometer: AccelerometerReading
    gyroscope: GyroscopeReading
