import random
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

# Import your models and database setup
from db.db_setup import engine, Base
from db.models.observation import Observation
from db.models.equipment import Equipment

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Equipment data
equipment_data = [
    {"id": "EQ-12495"},
    # Add more equipment if needed
]

# Insert equipment data
for equipment in equipment_data:
    equipment_instance = Equipment(id=equipment["id"])
    try:
        session.add(equipment_instance)
        session.commit()
    except OperationalError as e:
        print(f"Error inserting equipment: {e}")
        session.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()

# Define the time range
now = datetime.now(timezone.utc)
start_date = now - timedelta(days=60)  # Two months before
end_date = now

# Define the number of observations
num_hours = int((end_date - start_date).total_seconds() // 3600) + 1

# Generate and insert observations
for i in range(num_hours):
    timestamp = start_date + timedelta(hours=i)
    observation = Observation(
        id=i + 1,
        equipmentId="EQ-12495",  # Use the equipment ID from the inserted data
        timestamp=timestamp,
        value=round(random.uniform(50, 100), 2),
        flag="valid" 
    )
    try:
        session.add(observation)
        session.commit()
    except OperationalError as e:
        print(f"Error inserting observation: {e}")
        session.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
        
# Update the sequence for the 'observations_id_seq'
try:
    session.execute(
        text("SELECT setval('observations_id_seq', COALESCE((SELECT MAX(id) + 1 FROM observations), 1), false);")
    )
    session.commit()
except OperationalError as e:
    print(f"Error updating sequence: {e}")
    session.rollback()
except Exception as e:
    print(f"Unexpected error: {e}")
    session.rollback()

session.close()
