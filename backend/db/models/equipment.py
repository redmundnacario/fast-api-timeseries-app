from sqlalchemy import Column, Integer, String, orm

from .mixins import Timestamp
from ..db_setup import Base

class Equipment(Timestamp, Base):
  __tablename__ = "equipments"
  
  id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
  name = Column(String, nullable=True)