# FastAPI application for managing a word book with CRUD operations

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
# Create the database tables defined in Base's subclasses (i.e., models), using the engine.

app = FastAPI(title="WordBook API")
# Initialize FastAPI application with the title "WordBook API"


def get_db():
    db = SessionLocal()
    try:
        yield db
        # hands the session to the FastAPI, and stops here until the request is done
    finally:
        db.close()
        # when the request is done, close the DB session



@app.get("/words", response_model=list[schemas.WordRead])
def read_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_words(db, skip=skip, limit=limit)


@app.post("/words", response_model=schemas.WordRead)
def create_word(word_in: schemas.WordCreate, db: Session = Depends(get_db)):
    return crud.create_word(db, word_in)


@app.get("/words/{word_id}", response_model=schemas.WordRead)
def read_word(word_id: int, db: Session = Depends(get_db)):
    word = crud.get_word(db, word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@app.delete("/words/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_word(db, word_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"deleted": True}

