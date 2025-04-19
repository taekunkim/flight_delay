import os
import json

from datetime import datetime 
from sqlalchemy.orm import Session

from src.utils.logger import logger
from src.utils.db import SessionLocal

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
# Insert data to DB
# ───────────────────────────────
def insert_data_to_db(table: object, data: list[dict], upsert: bool=False):
    """
    Inserts a list of flight arrival dictionaries into the database.
    """
    from sqlalchemy.inspection import inspect
    from sqlalchemy.dialects.postgresql import insert

    session: Session = SessionLocal()

    cols = [col.name for col in inspect(table).c]
    pk_cols = [pk.name for pk in inspect(table).primary_key]
    updatable_columns = [col for col in cols if col not in pk_cols]

    if len(data) > 0:
        try:
            stmt = insert(table).values(data)
            if upsert:
                stmt = stmt.on_conflict_do_update(
                    index_elements=pk_cols,
                    set_={col: getattr(stmt.excluded, col) for col in updatable_columns}
                )

            session.execute(stmt)
            session.commit()

            if not upsert: 
                print(f"Inserted {len(data)} records.")
            if upsert: 
                print(f"Upserted {len(data)} records.")

        except Exception as e:
            logger.warning("Failed to upsert records: %s", e, exc_info=True)

        finally:
            session.close()

    else:
        logger.warning("No valid records to insert.")

    session.close()