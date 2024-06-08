import random
from typing import List, Tuple

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

    def fetch_eligible_mixes(self, contest_id: int):
        # This query fetches submissions and their respective contest results
        query = self.db.query(
            models.Submission.id,
            ContestResult.num_feedbacks,
            ContestResult.win_rate
        ).join(
            ContestResult, models.Submission.id == ContestResult.submission_id
        ).filter(
            ContestResult.contest_id == contest_id
        ).order_by(
            ContestResult.num_feedbacks.asc(),
            ContestResult.win_rate.asc()
        ).all()

        return query

    def select_head_to_head_mixes(self, contest_id: int) -> Tuple[int, int]:
        # Assumption: mixes is a list of tuples (submission_id, num_feedbacks, win_rate)
        mixes = self.fetch_eligible_mixes(contest_id)
        if len(mixes) < 2:
            raise ValueError("Not enough mixes for head-to-head comparison")

        # Filter mixes with the lowest number of feedbacks
        min_feedbacks = mixes[0][1]
        eligible_mixes = [mix for mix in mixes if mix[1] == min_feedbacks]

        # If there are not enough mixes with the same feedback count, broaden the criteria
        if len(eligible_mixes) < 2:
            next_min_feedbacks = mixes[1][1] if len(mixes) > 1 else min_feedbacks
            eligible_mixes.extend([mix for mix in mixes if mix[1] == next_min_feedbacks])

        # Randomly select two mixes from the eligible list
        selected_mixes = random.sample(eligible_mixes, 2)

        return selected_mixes[0][0], selected_mixes[1][0]

    def get_head_to_head_mixes(self, contest_id: int):
        try:
            mix1_id, mix2_id = self.select_head_to_head_mixes(contest_id)
            mix1_data = self.submissions_service.get_submission_by_id(mix1_id)
            mix2_data = self.submissions_service.get_submission_by_id(mix2_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return [mix1_data, mix2_data]

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

