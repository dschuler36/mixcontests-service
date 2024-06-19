from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased

from app.api import models


class ContestResultsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_contest_results_summary_for_contest_id(self, contest_id: int):
        SubmissionAlias = aliased(models.Submission)
        UserAlias = aliased(models.User)

        # Query the contest results and join the Submission and User tables
        contest_results = self.db.query(
            models.ContestResult,
            SubmissionAlias.id.label('submission_id'),
            UserAlias.username.label('username')
        ).join(
            SubmissionAlias, models.ContestResult.submission_id == SubmissionAlias.id
        ).join(
            UserAlias, SubmissionAlias.user_id == UserAlias.id
        ).filter(
            models.ContestResult.contest_id == contest_id
        ).order_by(
            models.ContestResult.win_rate.desc()
        ).all()

        num_results = 10
        filtered_contest_results = contest_results[0:num_results]  # Corrected slicing to include 10 results
        num_entries = len(contest_results)
        if not contest_results:
            raise HTTPException(status_code=404, detail="Contest results not found.")

        # Prepare the result with username included
        results_with_usernames = [
            {
                "contest_result_id": result.ContestResult.contest_results_id,
                "submission_id": result.submission_id,
                "username": result.username,
                "num_feedbacks": result.ContestResult.num_feedbacks,
                "win_rate": result.ContestResult.win_rate,
            }
            for result in filtered_contest_results
        ]

        return {
            "num_entries": num_entries,
            f"top_{num_results}_entries": results_with_usernames
        }