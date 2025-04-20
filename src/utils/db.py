import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")

db_url = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine + session factory
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
