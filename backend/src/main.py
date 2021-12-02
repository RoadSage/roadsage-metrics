import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .database import UserTable
from .routes.sso import router as sso_router
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
app.add_middleware(SessionMiddleware, secret_key="some-random-string")


# Set database config
os.environ["PICCOLO_CONF"] = "src.database_conf"

app.include_router(sso_router)
app.include_router(user_router)


@app.on_event("startup")
async def initialize_database() -> None:  # coverage: ignore
    await UserTable.create_table(if_not_exists=True).run()
