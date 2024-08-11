from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from db.db_setup import DATABASE_URL

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def reset_database():
    try:
        # Reflect the existing tables
        meta = MetaData()
        meta.reflect(bind=engine)

        # Drop all tables
        print("Dropping all tables...")
        meta.drop_all(bind=engine)
        print("All tables dropped successfully.")
        
    except OperationalError as e:
        print(f"OperationalError: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    reset_database()