# Database setup using SQLAlchemy

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# create_engine → creates the connection to the database
# sessionmaker → creates a factory to generate DB sessions
# declarative_base → base class for all ORM models (tables)



DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://wordbook_user@localhost:5432/wordbook",
)
# use Postgres



engine = create_engine(DATABASE_URL)

# -What is the engine?-
# The engine is the core connection object.
# SQLAlchemy uses it to open connections, execute queries, and talk to the DB.

# -Why check_same_thread=False?- (Only for SQLite)
# SQLite has a restriction:
# it doesn’t like being accessed from different threads.

# FastAPI uses asynchronous or threaded request handling.
# This flag disables the thread check so FastAPI can access SQLite safely.


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# -What is this?-
# It is a session factory.

# FastAPI will call this to create a new DB session per request.
# Meaning:
# 	•	autocommit=False → you must manually commit
# 	•	autoflush=False → SQLAlchemy won’t auto-run pending queries
# 	•	bind=engine → sessions use the engine created above


Base = declarative_base()
# Create a base class for "ORM models (tables)".
# when a class inherits from this, this "Base" class observes and registers it.


