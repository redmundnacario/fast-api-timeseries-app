from typing import List, Union
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

observations = []

class Observations (BaseModel):
    equipmentId: int
    timestamp: str
    value: float

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

@app.get("/parameters", response_model=List[Observations])
async def get_observations():
    return observations

@app.get("/observations", response_model=List[Observations])
async def get_observations():
    return observations

@app.post("/observations")
async def create_observation(observation: Observations):
    observations.append(observation)
    return "Observation Added"