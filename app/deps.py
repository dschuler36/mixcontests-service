from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.database import get_db
from app.api.services.contests_service import ContestsService
from app.api.services.gcs_service import GCSService
from app.api.services.feedback_service import FeedbackService
from app.api.services.submissions_service import SubmissionsService
from app.api.services.users_service import UsersService


def get_gcs_service() -> GCSService:
    return GCSService()


def get_contests_service(
        db: Session = Depends(get_db),
        gcs_service: GCSService = Depends(get_gcs_service)) -> ContestsService:
    return ContestsService(db, gcs_service)


def get_submissions_service(
        db: Session = Depends(get_db),
        gcs_service: GCSService = Depends(get_gcs_service)) -> SubmissionsService:
    return SubmissionsService(db, gcs_service)


def get_users_service(db: Session = Depends(get_db)) -> UsersService:
    return UsersService(db)


def get_feedback_service(
        db: Session = Depends(get_db),
        submissions_service: SubmissionsService = Depends(get_submissions_service)
) -> FeedbackService:
    return FeedbackService(db, submissions_service)
