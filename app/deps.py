from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.database import get_db
from app.api.services.contests_service import ContestsService
from app.api.services.ratings_service import RatingsService
from app.api.services.submissions_service import SubmissionsService


def get_contests_service(db: Session = Depends(get_db)) -> ContestsService:
    return ContestsService(db)


def get_submissions_service(db: Session = Depends(get_db)) -> SubmissionsService:
    return SubmissionsService(db)


def get_ratings_service(
        db: Session = Depends(get_db),
        submissions_service: SubmissionsService = Depends(get_submissions_service)
) -> RatingsService:
    return RatingsService(db, submissions_service)
