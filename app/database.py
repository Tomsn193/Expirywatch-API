import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load variables from a local .env file (ignored by git) into the environment.
load_dotenv()

# The database URL (which contains the password) must come from the environment.
# There is deliberately no default: credentials must never be hardcoded in the repo.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill in your values."
    )

# SQL logging is useful when debugging but noisy; keep it off unless SQL_ECHO=true.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

engine = create_engine(DATABASE_URL, echo=SQL_ECHO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """Dependency to get a database session for a request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
