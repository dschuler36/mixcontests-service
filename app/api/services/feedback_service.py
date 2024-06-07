from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas
from app.api.models import Feedback, ContestResult
from app.api.services.submissions_service import SubmissionsService


class FeedbackService:
    def __init__(self, db: Session, submissions_service: SubmissionsService):
        self.db = db
        self.submissions_service = submissions_service

    # def create_rating(self, rating: schemas.RatingCreate):
    #     submission_creator = self.submissions_service.get_submission_by_id(rating.submission_id).user_id
    #     if submission_creator == rating.rated_by:
    #         raise HTTPException(400, "User can't rate their own submission.")
    #     db_rating = models.Rating(**rating.dict())
    #     self.db.add(db_rating)
    #     self.db.commit()
    #     self.db.refresh(db_rating)
    #     return db_rating

    def get_submissions_for_feedback(self, contest_id):
        # Get two submissions with similar win rates
        pass

    def update_contest_results(self, feedback):
        for submission_id in [feedback.submission_1_id, feedback.submission_2_id]:
            result = self.db.query(ContestResult).filter(
                ContestResult.contest_id == feedback.contest_id,
                ContestResult.submission_id == submission_id
            ).first()

            if result:
                result.num_feedbacks += 1
                if submission_id == feedback.winner_submission_id:
                    result.win_rate = ((result.win_rate * (result.num_feedbacks - 1)) + 100) / result.num_feedbacks
                else:
                    result.win_rate = ((result.win_rate * (result.num_feedbacks - 1))) / result.num_feedbacks
                # SQLAlchemy will automatically call self.db.add(result) if the result already exists
            else:
                win_rate = 100.0 if submission_id == feedback.winner_submission_id else 0.0
                result = ContestResult(
                    contest_id=feedback.contest_id,
                    submission_id=submission_id,
                    num_feedbacks=1,
                    win_rate=win_rate
                )
                self.db.add(result)
        self.db.commit()
        return result

    def create_feedback(self, feedback):
        db_feedback = Feedback(**feedback.dict())
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)

        # Update contest_result table
        self.update_contest_results(feedback)
        return db_feedback

    def get_feedback_by_id(self, feedback_id):
        feedback = self.db.query(models.Feedback).filter(models.Feedback.feedback_id == feedback_id).first()
        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
        return feedback

