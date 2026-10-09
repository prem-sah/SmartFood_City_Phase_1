from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

from app.routers import (
    donors,
    receivers,
    food_donations,
    matching,
    volunteers,
    assignments,
    dashboard
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartFood City API",
    description="AI-powered surplus food management and redistribution platform",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(donors.router)
app.include_router(receivers.router)
app.include_router(food_donations.router)
app.include_router(matching.router)
app.include_router(volunteers.router)
app.include_router(assignments.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "project": "SmartFood City",
        "status": "running",
        "version": "0.4.0",
        "message": "Surplus food management platform API"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}