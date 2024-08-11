from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

from datetime import datetime

@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)