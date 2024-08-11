from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import observations

from config import get_settings
from db.db_setup import engine
from db.models import observation, equipment

observation.Base.metadata.create_all(bind=engine)
equipment.Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title="Observations",
    description="Observation data",
    version=f'{settings.APP_VERSION}',
    contact={
        "name": "Red",
        "email": "redmund.nacario@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

app.include_router(observations.router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}