import os

from utils.logger import logger
from utils.helper import read_data, insert_data_to_db
from db.models.flight_delay import FlightDelay


logger = logger


# ───────────────────────────────
# Fomat data
# ───────────────────────────────

def load_flight_arrivals_data(
        data: list[dict]
    ) -> list[dict]:
            
    # ───────────────────────────────
    # Load data
    # ───────────────────────────────
    insert_data_to_db(FlightDelay, data, upsert=True)
    
def main():
    ARRIVAL_API_CLEAN_DUMP_FILEPATH = os.getenv("ARRIVAL_API_CLEAN_DUMP_FILEPATH") 
    data = read_data(ARRIVAL_API_CLEAN_DUMP_FILEPATH)

    load_flight_arrivals_data(data)
    
if __name__ == "__main__":
    main()