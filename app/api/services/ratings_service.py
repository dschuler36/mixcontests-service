from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas
from app.api.services.submissions_service import SubmissionsService


class RatingsService:
    def __init__(self, db: Session, submissions_service: SubmissionsService):
        self.db = db
        self.submissions_service = submissions_service

    def create_rating(self, rating: schemas.RatingCreate):
        submission_creator = self.submissions_service.get_submission_by_id(rating.submission_id).user_id
        if submission_creator == rating.rated_by:
            raise HTTPException(400, "User can't rate their own submission.")
        db_rating = models.Rating(**rating.dict())
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating
