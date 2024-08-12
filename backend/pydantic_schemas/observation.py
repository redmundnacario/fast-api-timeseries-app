from typing import Literal
from pydantic import BaseModel
from datetime import datetime, timezone
import enum

class FlagEnum(enum.Enum):
    valid = "valid"
    missing = "missing"

class ObservationBase(BaseModel):
    equipmentId: str
    timestamp: datetime
    value: float
    flag: FlagEnum  # Use the Enum class directly

class ObservationCreate(ObservationBase):
    class Config: 
        schema_extra = {
            "examples": [
                {
                    "equipmentId": "EQ-12495",
                    "timestamp": "2023-02-12T06:30:00Z",
                    "value": 78.8,
                    "flag": "valid"
                }
            ]
        }
            

class Observation(ObservationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        }

    @staticmethod
    def utc_format(dt: datetime) -> str:
        return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def utc_raw_to_utc_format(dt: datetime) -> str:
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            equipmentId=obj.equipmentId,
            timestamp=cls.utc_format(obj.timestamp),
            created_at=cls.utc_raw_to_utc_format(obj.created_at),
            updated_at=cls.utc_raw_to_utc_format(obj.updated_at),
            value=obj.value,
            flag=obj.flag.value
        )
