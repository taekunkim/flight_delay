import os

from time import time


from utils.logger import logger
from utils.helper import insert_data_to_db

from db.models.flight_delay import FlightDelay
from etl.extract.flight_data import get_flight_delay_data
from etl.transform.flight_data import clean_flight_arrivals_data


API_BASE_URL = os.getenv("API_BASE_URL")
ARRIVAL_API_ENDPOINT = os.getenv("ARRIVAL_API_ENDPOINT")
API_KEY = os.getenv("API_KEY")


ARRIVAL_API_FLIGHT_CODE = os.getenv("ARRIVAL_API_FLIGHT_CODE")
ARRIVAL_API_FLIGHT_DATETIME_FROM = os.getenv("ARRIVAL_API_FLIGHT_DATETIME_FROM")
ARRIVAL_API_FLIGHT_DATETIME_TO = os.getenv("ARRIVAL_API_FLIGHT_DATETIME_TO")
ARRIVAL_API_RAW_DUMP_FILEPATH = os.getenv("ARRIVAL_API_RAW_DUMP_FILEPATH") 
ARRIVAL_API_CLEAN_DUMP_FILEPATH = os.getenv("ARRIVAL_API_CLEAN_DUMP_FILEPATH") 


# ───────────────────────────────
# Main Script Entry Point
# ───────────────────────────────
def main():
    main_func_start_time = time()

    # ───────────────────────────────
    # Fetch API Data
    # ───────────────────────────────
    logger.info("Extracting flight delay data via API...")

    delay_data_raw = get_flight_delay_data(ARRIVAL_API_FLIGHT_CODE, ARRIVAL_API_FLIGHT_DATETIME_FROM,  ARRIVAL_API_FLIGHT_DATETIME_TO, ARRIVAL_API_RAW_DUMP_FILEPATH)
    logger.info("Finished extracting Flight Arrival data via API.")

    logger.info("Transforming flight delay data...")
    delay_data_clean = clean_flight_arrivals_data(delay_data_raw, ARRIVAL_API_CLEAN_DUMP_FILEPATH)
    logger.info("Finished transforming flight delay data...")

    # insert data to db
    logger.info("Loading flight delay data to db...")
    insert_data_to_db(FlightDelay, delay_data_clean, upsert=True)
    logger.info("Finished loading flight delay data to db...")

    main_func_duration = round(time() - main_func_start_time, 2)
    logger.info(f"Main script completed in {main_func_duration} seconds.")
    
if __name__ == "__main__":
    main()