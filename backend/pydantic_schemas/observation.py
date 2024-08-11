from pydantic import BaseModel

from datetime import datetime, timezone

class ObservationBase (BaseModel):
    equipmentId: int
    timestamp: datetime
    value: float
    
class ObservationCreate(ObservationBase):
    ...
    
class ObservationAverage(ObservationBase):
    ...
    
class Observation (ObservationBase):
    ...
    id: int
    flag: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
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
            timestamp=cls.utc_format(obj.timestamp),  # Convert to UTC formatted string
            created_at=cls.utc_raw_to_utc_format(obj.created_at),
            updated_at=cls.utc_raw_to_utc_format(obj.updated_at),
            value=obj.value,
            flag=obj.flag
        )

    class Config:
        orm_mode = True
