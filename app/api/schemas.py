from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.api.enums import SubmissionState


class UserBase(BaseModel):
    idp_user_id: str
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


class EmailAddress(BaseModel):
    email_address: EmailStr


class UserCreatedData(BaseModel):
    id: str
    email_addresses: List[EmailAddress]
    username: Optional[str] = None


class UserUpdatedData(BaseModel):
    id: str
    email_addresses: Optional[List[EmailAddress]] = None
    username: Optional[str] = None


class UserDeletedData(BaseModel):
    id: str
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
    submission_url: str
    contest_id: int
    user_id: int
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
