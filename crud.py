# SQLAlchemy CRUD operations for Word model

from sqlalchemy.orm import Session

from models import Word
from schemas import WordCreate


def get_word(db: Session, word_id: int):
    return db.query(Word).filter(Word.id == word_id).first()


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Word).offset(skip).limit(limit).all()


def create_word(db: Session, word_in: WordCreate):
    db_word = Word(
        term=word_in.term,
        meaning=word_in.meaning,
        example=word_in.example,
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def delete_word(db: Session, word_id: int):
    word = get_word(db, word_id)
    if not word:
        return False
    db.delete(word)
    db.commit()
    return True

