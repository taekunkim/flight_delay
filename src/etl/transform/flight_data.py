import os

from utils.logger import logger
from utils.helper import read_data, dump_data
from sqlalchemy.inspection import inspect

from datetime import datetime, timezone

logger = logger

# ───────────────────────────────
# Fomat data
# ───────────────────────────────

def clean_flight_arrivals_data(
        raw_data: list[dict], 
        dump_filepath: str=None
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
        dump_data(clean_data, dump_filepath)

    return clean_data
    
def main():
    ARRIVAL_API_RAW_DUMP_FILEPATH = os.getenv("ARRIVAL_API_RAW_DUMP_FILEPATH") 
    ARRIVAL_API_CLEAN_DUMP_FILEPATH = os.getenv("ARRIVAL_API_CLEAN_DUMP_FILEPATH") 

    data = read_data(ARRIVAL_API_RAW_DUMP_FILEPATH)

    clean_flight_arrivals_data(
        data,
        ARRIVAL_API_CLEAN_DUMP_FILEPATH
    )
    
if __name__ == "__main__":
    main()
