from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # contests = relationship("Contest", back_populates="creator")
    submissions = relationship("Submission", back_populates="user")
    ratings = relationship("Rating", back_populates="rater")


class Contest(Base):
    __tablename__ = 'contests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    voting_start_date = Column(DateTime)
    voting_end_date = Column(DateTime)
    stem_url = Column(String)
    # created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # creator = relationship("User", back_populates="contests")
    submissions = relationship("Submission", back_populates="contest")


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey('contests.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    submission_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contest = relationship("Contest", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    ratings = relationship("Rating", back_populates="submission")


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'))
    rated_by = Column(Integer, ForeignKey('users.id'))
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="ratings")
    rater = relationship("User", back_populates="ratings")
