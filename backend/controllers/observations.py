from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from typing import Dict, List, Optional

from db.models.observation import Observation
from pydantic_schemas.observation import  ObservationCreate


def create_observations_controller(db: Session, observations: List[ObservationCreate]):
  try:
    
    # Convert the Pydantic models to SQLAlchemy model
    observation_instances = [
      Observation(
        equipmentId=obs.equipmentId,
        timestamp=obs.timestamp,
        value=obs.value,
        flag="valid"
      )
      for obs in observations
    ]

    # Add each observation instance to the session
    # for observation in observation_instances:
    db.add_all(observation_instances)
    
    # Commit the transaction
    db.commit()
    
    # Refresh observations_id_seq
    db.execute(text("SELECT setval('observations_id_seq', COALESCE((SELECT MAX(id) + 1 FROM observations), 1), false);"))
    db.commit()
  
  except SQLAlchemyError as e:
    # Rollback in case of error
    db.rollback()
    raise e

def get_observations_by_equipmentId_controller(
  db: Session, 
  equipmentId: int, 
  start_time: Optional[str] = None, 
  end_time: Optional[str] = None
) -> List[Observation]:
  
  query = db.query(Observation).filter(Observation.equipmentId == equipmentId)
  
  if start_time:
    query = query.filter(Observation.timestamp >= start_time)
  
  if end_time:
    query = query.filter(Observation.timestamp <= end_time)
        
  return query.all()