from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, Enum as SQLEnum, UUID, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from app.api.enums import SubmissionState

Base = declarative_base()


class AuthUser(Base):
    '''
    This is created to mimic the supabase auth.users table where user data is stored. This is so that the alembic
    migrations can successfully run. This table definition below will never try to get created.
    '''
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True), primary_key=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contests = relationship("Contest", back_populates="creator")
    submissions = relationship("Submission", back_populates="user")
    ratings = relationship("Feedback", back_populates="rater")


class Contest(Base):
    __tablename__ = 'contests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    submission_start_date = Column(DateTime)
    submission_end_date = Column(DateTime)
    voting_start_date = Column(DateTime)
    voting_end_date = Column(DateTime)
    stem_url = Column(String)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="contests")
    submissions = relationship("Submission", back_populates="contest")
    feedbacks = relationship("Feedback", back_populates="contest")
    contest_results = relationship("ContestResult", back_populates="contest")


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey('contests.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    submission_file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # state defines the current stage the user needs to complete, not what they've already completed
    state = Column(SQLEnum(SubmissionState, values_callable=lambda obj: [e.value for e in obj]))

    contest = relationship("Contest", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    feedbacks_1 = relationship('Feedback', foreign_keys='Feedback.submission_1_id', back_populates='submission_1')
    feedbacks_2 = relationship('Feedback', foreign_keys='Feedback.submission_2_id', back_populates='submission_2')
    feedbacks_won = relationship('Feedback', foreign_keys='Feedback.winner_submission_id', back_populates='winner_submission')
    contest_results = relationship('ContestResult', back_populates='submission')


class Feedback(Base):
    __tablename__ = 'feedback'

    feedback_id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)
    submission_1_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission_2_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    winner_submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    feedback_text_1 = Column(Text)
    feedback_text_2 = Column(Text)
    rater_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    contest = relationship('Contest', back_populates='feedbacks')
    submission_1 = relationship('Submission', foreign_keys=[submission_1_id], back_populates='feedbacks_1')
    submission_2 = relationship('Submission', foreign_keys=[submission_2_id], back_populates='feedbacks_2')
    winner_submission = relationship('Submission', foreign_keys=[winner_submission_id], back_populates='feedbacks_won')
    rater = relationship('User', back_populates='ratings')


class ContestResult(Base):
    __tablename__ = 'contest_results'

    contest_results_id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    num_feedbacks = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)

    contest = relationship('Contest', back_populates='contest_results')
    submission = relationship('Submission', back_populates='contest_results')