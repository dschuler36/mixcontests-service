from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import models
from app.api.config import settings
from app.api.database import engine
from app.api.routes import contests, feedback, submissions, users, gcs

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(contests.router)
app.include_router(feedback.router)
app.include_router(submissions.router)
app.include_router(users.router)
app.include_router(gcs.router)
