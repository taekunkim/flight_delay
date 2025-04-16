import os
import json

from scripts.db import SessionLocal

from datetime import datetime 
from scripts.logger import logger
from sqlalchemy.orm import Session

# ───────────────────────────────
# Logging Configuration
# ───────────────────────────────
logger = logger

# ───────────────────────────────
# Save JSON Output
# ───────────────────────────────
def dump_data(data: dict, output_dir: str, base_filename: str) -> None:
    """
    Saves json/dict data to local file.

    Args:
        data (dict): data to save.
        output_dir (str): directory to save the data in.
        base_filename (str): the name of file to save data to.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"{base_filename}_{timestamp}.json")
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
        logger.info(f"Saved API response to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")

# ───────────────────────────────
# Load data to DB
# ───────────────────────────────
def insert_data_to_db(data: list[dict]):
    """
    Inserts a list of flight arrival dictionaries into the database.
    """
    session: Session = SessionLocal()

    if len(data) > 0:
        logger.info(f"Inserting {len(data)} records of data to DB.")
        session.add_all(data)
        session.commit()
        logger.info(f"Inserted data.")
    else:
        logger.warning("No valid records to insert.")

    session.close()