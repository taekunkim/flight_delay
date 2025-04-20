import os

from time import time
from dotenv import load_dotenv

from src.utils.logger import logger
from src.utils.helper import insert_data_to_db

from src.db.models.flight_delay import FlightDelay
from src.etl.extract.flight_data import get_flight_delay_data
from src.etl.transform.flight_data import clean_flight_arrivals_data


# ───────────────────────────────
# Logging Configuration
# ───────────────────────────────
logger = logger

# ───────────────────────────────
# Load .env config
# ───────────────────────────────
load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
API_BASE_URL = os.getenv("API_BASE_URL")
ARRIVAL_API_ENDPOINT = os.getenv("ARRIVAL_API_ENDPOINT")
API_KEY = os.getenv("API_KEY")


ARRIVAL_API_FLIGHT_CODE = os.getenv("ARRIVAL_API_FLIGHT_CODE")
ARRIVAL_API_FLIGHT_DATETIME_FROM = os.getenv("ARRIVAL_API_FLIGHT_DATETIME_FROM")
ARRIVAL_API_FLIGHT_DATETIME_TO = os.getenv("ARRIVAL_API_FLIGHT_DATETIME_TO")
ARRIVAL_API_RAW_DUMP_FILE_NAME = os.getenv("ARRIVAL_API_RAW_DUMP_FILE_NAME") 
ARRIVAL_API_CLEAN_DUMP_FILE_NAME = os.getenv("ARRIVAL_API_CLEAN_DUMP_FILE_NAME") 


# ───────────────────────────────
# Main Script Entry Point
# ───────────────────────────────
def main():
    main_func_start_time = time()

    # ───────────────────────────────
    # Fetch API Data
    # ───────────────────────────────
    logger.info("Extracting flight delay data via API...")

    delay_data_raw = get_flight_delay_data(ARRIVAL_API_FLIGHT_CODE, ARRIVAL_API_FLIGHT_DATETIME_FROM,  ARRIVAL_API_FLIGHT_DATETIME_TO, ARRIVAL_API_RAW_DUMP_FILE_NAME)
    # from pathlib import Path
    # import json
    # with Path("../data/flight_data/flight_delay_raw.json").open("r", encoding="utf-8") as f:
    #     delay_data_raw = json.load(f)
    logger.info("Finished extracting Flight Arrival data via API.")

    logger.info("Transforming flight delay data...")
    delay_data_clean = clean_flight_arrivals_data(delay_data_raw, ARRIVAL_API_CLEAN_DUMP_FILE_NAME)
    logger.info("Finished transforming flight delay data...")

    # insert data to db
    logger.info("Loading flight delay data to db...")
    insert_data_to_db(FlightDelay, delay_data_clean, upsert=True)
    logger.info("Finished loading flight delay data to db...")

    main_func_duration = round(time() - main_func_start_time, 2)
    logger.info(f"Main script completed in {main_func_duration} seconds.")
    
if __name__ == "__main__":
    main()