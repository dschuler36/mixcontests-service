from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas


class UsersService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: schemas.User):
        db_user = models.User(username=user.username, email=user.email, password_hash=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
