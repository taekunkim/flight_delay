import json
from pathlib import Path
from datetime import datetime 
from sqlalchemy.orm import Session

from utils.logger import logger
from utils.db import SessionLocal, engine

# ───────────────────────────────
# Save JSON Output
# ───────────────────────────────
def dump_data(data: dict, filepath: str) -> None:
    """
    Saves json/dict data to local file.

    Args:
        data (dict): data to save.
        filepath (str): filepath to save the data to.
    """
    logger.info(f"Dumping {len(data):,} rows of data to {filepath}")
    try:
        # Create the directory if it doesn't exist
        filedir = Path(filepath).parent
        filedir.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(data, f)
        logger.info(f"Successfully dumped API response to {filepath}")
    except Exception as e:
        logger.error(f"Failed to dump file: {e}")

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
    updatable_columns.remove("ingested_at")

    # drop columns not found in the table, but foud in data
    clean_data = []
    for each in data:
        clean_data_i = {}
        for col in cols:
            clean_data_i[col] = each[col]
        clean_data.append(clean_data_i)

    if len(clean_data) > 0:
        try:
            stmt = insert(table).values(clean_data)
            if upsert:
                stmt = stmt.on_conflict_do_update(
                    index_elements=pk_cols,
                    set_={col: getattr(stmt.excluded, col) for col in updatable_columns}
                )

            session.execute(stmt)
            session.commit()

            if not upsert: 
                print(f"Inserted {len(clean_data)} records.")
            if upsert: 
                print(f"Upserted {len(clean_data)} records.")

        except Exception as e:
            logger.warning("Failed to upsert records: %s", e, exc_info=True)

        finally:
            session.close()

    else:
        logger.warning("No valid records to insert.")

    session.close()