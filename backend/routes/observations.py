import fastapi
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from datetime import datetime
from typing import List, Optional

from controllers.observations import create_observations_controller, get_observations_by_equipmentId_controller
from db.db_setup import get_db
from pydantic_schemas.observation import Observation, ObservationCreate

router = fastapi.APIRouter()

tag= "Observations"

@router.get("/observations/{equipmentId}", response_model=List[Observation], tags=["Observations"])
async def get_observations_by_equipmentId(
    equipmentId: int,
    start_time: Optional[datetime] = Query(None, description="Start time for filtering observations"),
    end_time: Optional[datetime] = Query(None, description="End time for filtering observations"),
    db: Session = Depends(get_db)
):
    try:
        observations = get_observations_by_equipmentId_controller(db, equipmentId, start_time, end_time)
        
        if not observations:
            raise HTTPException(status_code=404, detail="No observations found")
        
        return [Observation.from_orm(obs) for obs in observations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/observations", tags=[tag])
async def create_observation(observations: List[ObservationCreate], db: Session = Depends(get_db)):
    try: 
        create_observations_controller(db, observations)
        return {"Observations successfully added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))