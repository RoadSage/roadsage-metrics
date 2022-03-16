from datetime import datetime
from typing import Dict, Literal, Optional, Union

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


class UpdatePasswordRequest(BaseModel):
    new_password: str


class GoogleLoginRequest(BaseModel):
    token: str


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

    @staticmethod
    def from_database_dictionary(
        dict: Dict[str, Union[float, str, datetime]]
    ) -> "SensorReading":
        return SensorReading(
            timestamp=dict["timestamp"],
            text_displayed=dict["text_displayed"],
            lidar_distance=dict["lidar_distance"],
            ultrasonic_distance=dict["ultrasonic_distance"],
            accelerometer=AccelerometerReading(
                x=dict["accelerometer_x"],
                y=dict["accelerometer_y"],
                z=dict["accelerometer_z"],
            ),
            gyroscope=GyroscopeReading(
                x=dict["gyroscope_x"],
                y=dict["gyroscope_y"],
                z=dict["gyroscope_z"],
            ),
        )


class AppCommand(BaseModel):
    timestamp: datetime
    command: str
    invocation_method: Union[Literal["touch"], Literal["voice"]]
