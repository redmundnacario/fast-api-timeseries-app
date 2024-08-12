from sqlalchemy import Column, String, orm

from .mixins import Timestamp
from ..db_setup import Base

class Equipment(Timestamp, Base):
  __tablename__ = "equipments"
  
  id = Column(String, primary_key=True, index=True, unique=True)
  
  observations = orm.relationship("Observation", back_populates="equipment")