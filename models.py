# Base SQLAlchemy model for the "words" table

from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class Word(Base):
#     This creates a Python class that represents a database table.
# Base tells SQLAlchemy that this class should be mapped to a table.

    __tablename__ = "words"
# The name of the table in SQLite will be:　words

    id = Column(Integer, primary_key=True, index=True)
        # Integer column
        # Primary key (unique ID)
        # Indexed for faster lookup
    term = Column(String, index=True, nullable=False)
        # The English word itself
        # String type
        # Indexed (searching becomes faster)
        # nullable=False → cannot be empty
    meaning = Column(String, nullable=False)
        # Japanese meaning
        # Required field
        # example
        # example = Column(String, nullable=True)
    example = Column(String, nullable=True)
        # Optional example sentence
        # Can be null
    created_at = Column(DateTime(timezone=True), server_default=func.now())
        # Stores the timestamp when the row is created
        # Automatically filled by the database using NOW()
        # This means you don’t need to manually set it when inserting a word.