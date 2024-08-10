from typing import List
from schemas.observations import Observations

import fastapi

router = fastapi.APIRouter()

observations = []
tag= "Observations"

@router.get("/observations", response_model=List[Observations], tags =[tag])
async def get_observations():
    return observations

@router.post("/observations", tags=[tag])
async def create_observation(observation: Observations):
    observations.append(observation)
    return "Observation Added"