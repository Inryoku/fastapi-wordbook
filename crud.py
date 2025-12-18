# SQLAlchemy CRUD operations for Word model

# Each function receives:"db: Session"
# This is the active database session created in main.py.

from sqlalchemy.orm import Session

from models import Word
from schemas import WordCreate
	# •Session → type hint for SQLAlchemy session
	# •Word → the ORM model (the table)
	# •WordCreate → the Pydantic schema for creating a word

def get_word(db: Session, word_id: int):
    return db.query(Word).filter(Word.id == word_id).first()
# Purpose:
# Retrieve a single row from the database by its ID.

# Technical details:
# 	•	db.query(Word) → SELECT from the words table
# 	•	.filter(Word.id == word_id) → WHERE id = word_id
# 	•	.first() → return first match, or None if not found


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Word).offset(skip).limit(limit).all()
# Purpose:
# Retrieve multiple rows, with optional pagination.

# Behavior:
# 	•	offset(skip) → skip this many rows
# 	•	limit(limit) → maximum number of rows to return
# 	•	.all() → return the list


def create_word(db: Session, word_in: WordCreate):
    db_word = Word(
        term=word_in.term,
        meaning=word_in.meaning,
        example=word_in.example,
        part_of_speech=word_in.part_of_speech,
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word
# Purpose:
# Create a new row in the database.

# Step-by-step:
# 	1.	Build a new ORM object
# 	2.	Add it to the session
# 	3.	Commit the transaction
# 	4.	Refresh the object to get DB-generated fields (e.g., id, created_at)


def delete_word(db: Session, word_id: int):
    word = get_word(db, word_id)
    if not word:
        return False
    db.delete(word)
    db.commit()
    return True

