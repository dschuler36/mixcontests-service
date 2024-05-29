from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api import models
from app.api import schemas


class ContestsService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_contests(self):
        contests = self.db.query(models.Contest).all()
        return contests

    def get_contest_by_id(self, contest_id: int):
        contest = self.db.query(models.Contest).filter(models.Contest.id == contest_id).first()
        if not contest:
            raise HTTPException(status_code=404, detail="Contest not found")
        return contest

    def create_contest(self, contest: schemas.ContestCreate):
        db_contest = models.Contest(**contest.dict())
        self.db.add(db_contest)
        self.db.commit()
        self.db.refresh(db_contest)
        return db_contest
