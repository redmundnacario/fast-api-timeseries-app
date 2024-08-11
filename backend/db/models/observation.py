from sqlalchemy import orm
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Enum

import enum

from .mixins import Timestamp
from ..db_setup import Base

class flag(enum.Enum):
  valid = 1
  missing = 2

class Observation(Timestamp, Base):
  __tablename__ = "observations"
  
  id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
  equipmentId = Column(Integer, ForeignKey("equipments.id"), nullable=False, index=True)
  timestamp = Column(DateTime, nullable=False, index=True)
  value= Column(Float)
  flag= Column(Enum(flag), nullable=False, index=True)
  
  equipment = orm.relationship("Equipment")