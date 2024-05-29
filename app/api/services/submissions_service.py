from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas


class SubmissionsService:
    def __init__(self, db: Session):
        self.db = db

    def create_submission(self, submission: schemas.SubmissionCreate):
        db_submission = models.Submission(**submission.dict())
        self.db.add(db_submission)
        self.db.commit()
        self.db.refresh(db_submission)
        return db_submission

    def get_submission_by_id(self, submission_id: int):
        submission = self.db.query(models.Submission).filter(models.Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        return submission
