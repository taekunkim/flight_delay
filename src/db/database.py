# src/db/database.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Create a central Base class for all models to inherit from
Base = declarative_base()

# Optional: setup engine using environment variables (or config)
# This is used for direct script access (not needed if only Alembic handles connections)
DB_URL = os.getenv("DATABASE_URL")  # e.g., postgresql://user:pass@host:5432/dbname
engine = create_engine(DB_URL) if DB_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
