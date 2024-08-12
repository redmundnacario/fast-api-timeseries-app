import fastapi
from fastapi import Body, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from controllers.observations import create_observations_controller, get_observations_by_equipmentId_controller
from db.db_setup import get_db
from pydantic_schemas.observation import Observation, ObservationCreate

router = fastapi.APIRouter()

tag= "Observations"

# Helper function to get static example values
def get_static_example_times():
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    return {
        "start_time": one_hour_ago.isoformat() + 'Z',
        "end_time": now.isoformat() + 'Z'
    }

# Get static example values
example_times = get_static_example_times()

@router.get("/observations/{equipmentId}", response_model=List[Observation], tags=["Observations"])
async def get_observations_by_equipmentId(
    equipmentId: str = Path(..., description="ID of the equipment", example="EQ-12495"),
    start_time: Optional[datetime] = Query(None, description="Start time for filtering observations", example=example_times["start_time"]),
    end_time: Optional[datetime] = Query(None, description="End time for filtering observations", example=example_times["end_time"]),
    db: Session = Depends(get_db)
):
    try:
        observations = get_observations_by_equipmentId_controller(db, equipmentId, start_time, end_time)
        if not observations:
            raise HTTPException(status_code=404, detail="No observations found")
        
        return [Observation.from_orm(obs) for obs in observations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/observations", tags=[tag], response_model=Dict[str, str])
async def create_observation(observations: List[ObservationCreate] = Body(
        ...,
        example = [
                    {
                        "equipmentId": "EQ-12495",
                        "timestamp": "2023-02-12T06:30:00Z",
                        "value": 78.8,
                        "flag": "valid"
                    },
                    {
                        "equipmentId": "EQ-12492",
                        "timestamp": "2023-01-12T06:30:00Z",
                        "value": 8.8,
                        "flag": "missing"
                    }
                ]
            
), db: Session = Depends(get_db)):
    try: 
        create_observations_controller(db, observations)
        return {"message": "Observations successfully added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))