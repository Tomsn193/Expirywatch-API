import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load the database URL from the environment (defaulting for safety)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://expirywatch_user:Q7n4Vx9mK2pL8sR5cT3wY6bH1jF0dA@localhost:5444/expirywatch_db")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker to yield database sessions
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