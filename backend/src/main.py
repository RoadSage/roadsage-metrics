import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .routes.users import router as user_router

app = FastAPI(
    title="Roadsage - Metrics",
    description="An API to collect and store sensor data and usage metrics from the Roadsage app and display.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Set database config
os.environ["PICCOLO_CONF"] = "src.database_conf"


app.include_router(user_router)
