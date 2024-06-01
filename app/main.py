from fastapi import FastAPI
from ngrok import ngrok
from starlette.middleware.cors import CORSMiddleware

from app.api import models
from app.api.config import settings
from app.api.database import engine
from app.api.routes import contests, ratings, submissions, users

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
app.include_router(ratings.router)
app.include_router(submissions.router)
app.include_router(users.router)

print(settings)

if settings.ENV == "local":
    # expose localhost to internet to test webhook user events
    listener = ngrok.forward("localhost:8000", authtoken_from_env=True,
                             verify_webhook_provider="clerk",
                             verify_webhook_secret=settings.WEBHOOK_SECRET)



