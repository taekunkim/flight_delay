import os

from time import time
from dotenv import load_dotenv

from scripts.logger import logger
from scripts.utils import insert_data_to_db
from scripts.models.flight_arrivals import FlightArrival
from scripts.get_flight_arrival_data import get_flight_arrival_data

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

ARRIVAL_AIRPORT = os.getenv("ARRIVAL_AIRPORT") 
AIRLINE_CODE = os.getenv("AIRLINE_CODE")
FLIGHT_NUMBER = os.getenv("FLIGHT_NUMBER")
DATE_FROM = os.getenv("DATE_FROM") 
DATE_TO = os.getenv("DATE_TO") 
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
    arrival_data = get_flight_arrival_data(API_KEY, ARRIVAL_AIRPORT, AIRLINE_CODE, FLIGHT_NUMBER, DATE_FROM, DATE_TO)
    logger.info("Finished fetching Flight Arrival data via API.")

    # insert data to db
    insert_data_to_db(FlightArrival, arrival_data, upsert=True)

    main_func_duration = round(time() - main_func_start_time, 2)
    logger.info(f"Main script completed in {main_func_duration} seconds.")
    
if __name__ == "__main__":
    main()