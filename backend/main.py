from fastapi import FastAPI
from pydantic import BaseModel

from routes import observations

app = FastAPI(
    title="Observations",
    description="Observation data",
    version="0.0.1",
    contact={
        "name": "Red",
        "email": "redmund.nacario@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(observations.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}