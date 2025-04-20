import os

from time import time
from dotenv import load_dotenv

from src.utils.logger import logger
from src.utils.helper import insert_data_to_db
from src.db.models.flight_arrivals import FlightArrival
from src.etl.extract.flight_data import get_flight_arrival_data

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
ARRIVAL_API_FILE_NAME = os.getenv("ARRIVAL_API_FILE_NAME") 

# ───────────────────────────────
# Main Script Entry Point
# ───────────────────────────────
def main():
    main_func_start_time = time()

    # ───────────────────────────────
    # Fetch API Data
    # ───────────────────────────────
    logger.info("Fetching Flight Arrival data via API...")

    arrival_data = get_flight_arrival_data(ARRIVAL_API_FLIGHT_CODE, ARRIVAL_API_FLIGHT_DATETIME_FROM,  ARRIVAL_API_FLIGHT_DATETIME_TO, ARRIVAL_API_FILE_NAME)
    logger.info("Finished fetching Flight Arrival data via API.")

    # insert data to db
    insert_data_to_db(FlightArrival, arrival_data, upsert=True)

    main_func_duration = round(time() - main_func_start_time, 2)
    logger.info(f"Main script completed in {main_func_duration} seconds.")
    
if __name__ == "__main__":
    main()