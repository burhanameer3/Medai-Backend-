from fastapi import FastAPI
from .db.base import engine, Base
from app.routers import users,clients
from fastapi.middleware.cors import CORSMiddleware
from . import models  # noqa: F401 - Import models so SQLAlchemy knows about them

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple FastAPI Auth Example")
app.include_router(users.router)
app.include_router(clients.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)