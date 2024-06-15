from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api import models


class ContestResultsService:
    def __init__(self, db: Session):
        self.db = db

    def get_results_for_contest_id(self, contest_id: int):
        contest_results = self.db.query(models.ContestResult) \
                                 .filter(models.ContestResult.contest_id == contest_id) \
                                 .order_by(models.ContestResult.win_rate.desc()) \
                                 .all()
        if not contest_results:
            raise HTTPException(status_code=404, detail="Contest results not found.")

        return contest_results



