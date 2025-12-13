# Base SQLAlchemy model for the "words" table

from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True, nullable=False)
    meaning = Column(String, nullable=False)
    example = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

