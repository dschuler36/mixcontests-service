from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.api.enums import SubmissionState


class UserBase(BaseModel):
    id: UUID
    username: str
    email: str


class User(UserBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EmailAddress(BaseModel):
    email_address: EmailStr


class UserCreatedData(BaseModel):
    id: UUID
    email_addresses: List[EmailAddress]
    username: Optional[str] = None


class UserUpdatedData(BaseModel):
    id: UUID
    email_addresses: Optional[List[EmailAddress]] = None
    username: Optional[str] = None


class UserDeletedData(BaseModel):
    id: UUID
    deleted: bool


class UserCreatedEvent(BaseModel):
    type: str
    data: UserCreatedData


class UserUpdatedEvent(BaseModel):
    type: str
    data: UserUpdatedData


class UserDeletedEvent(BaseModel):
    type: str
    data: UserDeletedData


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
    submission_file_path: str
    contest_id: int
    user_id: UUID
    state: SubmissionState


class SubmissionCreate(SubmissionBase):
    pass


class Submission(SubmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

class FeedbackCreate(BaseModel):
    contest_id: int
    submission_1_id: int
    submission_2_id: int
    winner_submission_id: int
    rater_user_id: UUID
    feedback_text_1: Optional[str] = None
    feedback_text_2: Optional[str] = None