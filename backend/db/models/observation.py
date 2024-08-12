from sqlalchemy import orm
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Enum, String

import enum

from .mixins import Timestamp
from ..db_setup import Base

class Flag(enum.Enum):
  valid = "valid"
  missing = "missing"

class Observation(Timestamp, Base):
  __tablename__ = "observations"
  
  id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
  equipmentId = Column(String, ForeignKey("equipments.id"), nullable=True, index=True)
  timestamp = Column(DateTime, nullable=False, index=True)
  value= Column(Float)
  flag= Column(Enum(Flag), nullable=False, index=True)
  
  equipment = orm.relationship("Equipment", back_populates="observations")