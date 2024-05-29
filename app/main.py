from fastapi import FastAPI

from app.api import models
from app.api.database import engine
from app.api.routes import contests, ratings, submissions, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contests.router)
app.include_router(ratings.router)
app.include_router(submissions.router)
app.include_router(users.router)






