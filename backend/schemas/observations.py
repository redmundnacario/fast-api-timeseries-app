from pydantic import BaseModel

class Observations (BaseModel):
    equipmentId: int
    timestamp: str
    value: float
