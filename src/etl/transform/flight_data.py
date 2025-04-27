import os
import requests

from utils.logger import logger
from utils.helper import dump_data
from sqlalchemy.inspection import inspect

from datetime import datetime, timezone


logger = logger


# ───────────────────────────────
# Fomat data
# ───────────────────────────────

def clean_flight_arrivals_data(
        raw_data: list[dict], 
        dump_filename: str=None
    ) -> list[dict]:
    """

    """
    from db.models.flight_delay import FlightDelay
    pk_cols = [pk.name for pk in inspect(FlightDelay).primary_key]

    clean_data = []
    for each in raw_data:
        clean_data_i = {
            "flight_cd": each["flight"],
            "takeoff_dtm": each["datetime_takeoff"],
            "landing_dtm": each["datetime_landed"],
            "ingested_at": str(datetime.now(tz=timezone.utc)),
        }

        # check if data entry has all the PKs
        pk_missing = False
        for pk in pk_cols:
            if clean_data_i[pk] is None:
                pk_missing = True
        if not pk_missing:
            clean_data.append(clean_data_i)
            
    # ───────────────────────────────
    # Dump raw data
    # ───────────────────────────────
    DUMP_CLEAN_DATA = os.getenv("DUMP_CLEAN_DATA")
    if DUMP_CLEAN_DATA:
        OUTPUT_DIR = os.getenv("OUTPUT_DIR")
        ARRIVAL_API_CLEAN_DUMP_FILE_NAME = os.getenv("ARRIVAL_API_CLEAN_DUMP_FILE_NAME")
        dump_filepath = f"{OUTPUT_DIR}{ARRIVAL_API_CLEAN_DUMP_FILE_NAME}"
        dump_data(clean_data, dump_filepath)

    return clean_data
    
# ───────────────────────────────
# Prepare data for SQLAlchemy
# ───────────────────────────────
        
    # logger.info("Transforming data for SQLAlchemy")

    # clean_data = []
    # skip_counter = 0 # number of records skipped while parsing
    # for each in raw_data:
    #     try:
    #         clean_each = {
    #             "airline_iata_code": each.get("airline").get("iataCode"),
    #             "flight_number": each.get("flight").get("number"),
    #             "scheduled_arrival": datetime.fromisoformat(each.get("arrival").get("scheduledTime").replace("t", "T")),
    #             "actual_arrival": datetime.fromisoformat(each.get("arrival").get("actualTime").replace("t", "T")),
    #             "departure_delay": each.get("departure").get("delay"),
    #         }
    #         clean_data.append(clean_each)

    #     except Exception as e:
    #         skip_counter += 1
        
    # logger.warning(f"Skipped parsing {skip_counter} records due to invalid data.")

    # logger.info("Finished transforming data for SQLAlchemy")
