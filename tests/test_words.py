import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import os
import sys
from pathlib import Path

# Ensure project root is on sys.path for CI
sys.path.append(str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import main
from database import Base

# Use an in-memory SQLite database for isolated tests.
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # keep the same connection alive for the duration of the tests
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# when main.get_db is called, override_get_db will be called instead
main.app.dependency_overrides[main.get_db] = override_get_db

# Create tables once; they will be recreated per test by the autouse fixture below.
Base.metadata.create_all(bind=test_engine)

# fake http client for testing, as if someone is sending requests to the FastAPI app
client = TestClient(main.app)


# when each test function is run, this will run automatically.
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_create_and_read_word():
    payload = {
        "term": "apple",
        "meaning": "a fruit",
        "example": "An apple a day keeps the doctor away.",
        "part_of_speech": "noun",
    }

    # store the created word's response for further checks
    create_resp = client.post("/words", json=payload)
    # check if the response succeeded
    assert create_resp.status_code == 200
    # change the response python data
    created = create_resp.json()
    # check if the created word matches the payload
    assert created["term"] == payload["term"]
    assert created["meaning"] == payload["meaning"]
    assert created["example"] == payload["example"]
    assert created["part_of_speech"] == payload["part_of_speech"]
    # check if an ID is created in the server side
    assert isinstance(created["id"], int)


    list_resp = client.get("/words")
    assert list_resp.status_code == 200
    words = list_resp.json()
    assert len(words) == 1
    assert words[0]["term"] == payload["term"]

    get_resp = client.get(f"/words/{created['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == created["id"]
    assert fetched["term"] == payload["term"]


def test_delete_word():
    payload = {"term": "test", "meaning": "to try", "example": None, "part_of_speech": None}
    created = client.post("/words", json=payload).json()
    word_id = created["id"]

    del_resp = client.delete(f"/words/{word_id}")
    assert del_resp.status_code == 200
    assert del_resp.json() == {"deleted": True}

    missing_resp = client.get(f"/words/{word_id}")
    assert missing_resp.status_code == 404

    repeat_del_resp = client.delete(f"/words/{word_id}")
    assert repeat_del_resp.status_code == 404
