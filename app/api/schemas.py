from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContestBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    submission_start_date: datetime
    submission_end_date: datetime
    voting_start_date: datetime
    voting_end_date: datetime
    stem_url: str


class ContestCreate(ContestBase):
    pass


class ContestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    stem_url: Optional[str] = None


class Contest(ContestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SubmissionBase(BaseModel):
    submission_url: str
    contest_id: int
    user_id: int

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RatingBase(BaseModel):
    submission_id: int
    rated_by: int
    score: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
