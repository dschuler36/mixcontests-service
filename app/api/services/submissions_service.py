from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas


class SubmissionsService:
    def __init__(self, db: Session):
        self.db = db

    def create_submission(self, submission: schemas.SubmissionCreate):
        try:
            existing_submission = self.get_submission_by_user_and_contest(submission.user_id, submission.contest_id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User has already submitted to this contest")
        except HTTPException as e:
            if e.status_code != status.HTTP_404_NOT_FOUND:
                raise e

        db_submission = models.Submission(**submission.dict())
        self.db.add(db_submission)
        self.db.commit()
        self.db.refresh(db_submission)
        return db_submission

    def get_submission_by_id(self, submission_id: int):
        submission = self.db.query(models.Submission).filter(models.Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
        return submission

    def get_submission_by_user_and_contest(self, user_id, contest_id):
        submission = self.db.query(models.Submission).filter(
            models.Submission.user_id == user_id,
            models.Submission.contest_id == contest_id
        ).first()

        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        return submission
