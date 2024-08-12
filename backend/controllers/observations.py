from fastapi import HTTPException
from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from typing import Dict, List, Optional

from db.models.equipment import Equipment
from db.models.observation import Observation
from pydantic_schemas.observation import  FlagEnum, ObservationCreate

def create_observations_controller(db: Session, observations: List[ObservationCreate]):
  try:
    
    # Extract unique equipment IDs from observations
    equipment_ids = set(obs.equipmentId for obs in observations)

    # Check if these equipments already exist
    existing_equipments = db.query(Equipment).filter(Equipment.id.in_(equipment_ids)).all()
    existing_equipment_ids = {equip.id for equip in existing_equipments}

    # Create new equipment instances if needed
    new_equipments = [
        Equipment(id=equip_id)  # Assuming `id` is a required field for Equipment
        for equip_id in equipment_ids
        if equip_id not in existing_equipment_ids
    ]

    # Add new equipment instances to the session
    if new_equipments:
      db.add_all(new_equipments)
      db.commit()  # Commit to ensure new equipment is added before creating observations

    # Convert the Pydantic models to SQLAlchemy model instances
    observation_instances = []
    for obs in observations:
      # Convert the flag to the SQLAlchemy Enum type
      observation_instance = Observation(
          equipmentId=obs.equipmentId,
          timestamp=obs.timestamp,
          value=obs.value,
          flag=obs.flag.value
      )
      observation_instances.append(observation_instance)

    # Add the observation instances to the session
    db.add_all(observation_instances)
    
    # Commit the transaction
    db.commit()
    
    # Refresh observations_id_seq
    db.execute(text("SELECT setval('observations_id_seq', COALESCE((SELECT MAX(id) + 1 FROM observations), 1), false);"))
    db.commit()
  
  except SQLAlchemyError as e:
    # Rollback in case of error
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))

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