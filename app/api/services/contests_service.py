from datetime import datetime

from fastapi import HTTPException, status
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

    def update_contest(self, contest_id, contest):
        db_contest = self.db.query(models.Contest).filter(models.Contest.id == contest_id).first()
        if db_contest is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contest not found")

        # if db_contest.created_by != current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this contest")

        for key, value in contest.dict(exclude_unset=True).items():
            setattr(db_contest, key, value)

        self.db.commit()
        self.db.refresh(db_contest)
        return db_contest

    def delete_contest(self, contest_id):
        db_contest = self.db.query(models.Contest).filter(models.Contest.id == contest_id).first()
        if db_contest is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contest not found")

        # if db_contest.created_by != current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this contest")

        self.db.delete(db_contest)
        self.db.commit()
        return db_contest

    def get_active_contest(self):
        current_time = datetime.utcnow()
        active_contest = self.db.query(models.Contest).filter(
          models.Contest.start_date <= current_time, models.Contest.end_date >= current_time
        ).first()
        print(active_contest)

        if not active_contest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active contest found")

        return active_contest
