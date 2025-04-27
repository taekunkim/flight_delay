import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.getenv("APP_DB_URL")
if not db_url:
    raise ValueError("POSTGRES_URL environment variable not set")

# Create SQLAlchemy engine + session factory
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
