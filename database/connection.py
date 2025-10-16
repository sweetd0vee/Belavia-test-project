from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For local development, you can uncomment this line:
SQLALCHEMY_DATABASE_URL = "postgresql://sweetd0ve:sweetd0ve@127.0.0.1:5432/sweetd0ve"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure session factory: disable autocommit and autoflush for explicit control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Provide a SQLAlchemy database session generator for dependency injection.
    This ensures the session is properly closed after use.
    """
    return db
