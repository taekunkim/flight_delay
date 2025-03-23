import os
import json
import logging
from time import time
from dotenv import load_dotenv
from urllib.parse import urljoin, urlencode
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import requests
from datetime import datetime

# ───────────────────────────────
# Logging Configuration
# ───────────────────────────────
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


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
# API Function
# ───────────────────────────────
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff: 2s, 4s, 8s...
    stop=stop_after_attempt(3),                          # Retry up to 3 times
    retry=retry_if_exception_type(requests.RequestException),  # Retry only on request errors
    reraise=True,  # Raise final exception if all retries fail
    before_sleep=logger,  # Log each retry attempt
    after=logger.info("Retry attempt complete.")  # Optional hook
)
def get_arrival_info(
        api_key: str, 
        arrival_airport: str, 
        airline_code: str, 
        flight_number: str, 
        start_date_str: str, 
        end_date_str: str
    ) -> dict:
    """
    Via API, fetches arrival flight data for a given airport, airline, and flight number.

    Args:
        api_key (str): API credential key
        arrival_airport (str): The IATA code of the arrival airport (e.g., 'JFK').
        airline_code (str): The IATA code of the airline (e.g., 'AA').
        flight_number (str): The flight number to look up.
        date_from_str (str): The starting date for the query in 'YYYY-MM-DD' format.
            - If `end_date` is not provided, this is treated as a single-day search.
            - If `end_date` is provided, this marks the beginning of the date range.
        date_to_str (str): The end date for the query in 'YYYY-MM-DD' format.
            If provided, the search includes all dates from `start_date` to `end_date`, inclusive.

    Returns:
        dict: Parsed JSON response from the API.
    """
    logger.info("Preparing API request for flight arrivals")

    query_params = {
        "key": api_key,
        "code": arrival_airport,
        "type": "arrival",
        "date_from": start_date_str,
        "airline_iata": airline_code,
        "flight_num": flight_number,
    }
    if end_date_str is not None:
        query_params["date_to"] = end_date_str


    api_full_path = urljoin(API_BASE_URL, ARRIVAL_API_ENDPOINT)
    query_string = urlencode(query_params)
    api_url = f"{api_full_path}?{query_string}"

    logger.debug(f"Request URL: {api_url}")

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info(f"API call successful, status code {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise # raise error for retry
    
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
# Main Script Entry Point
# ───────────────────────────────
def main():
    main_func_start_time = time()
    logger.info("Flight arrival extraction started")
    arrival_info = get_arrival_info(API_KEY, ARRIVAL_AIRPORT, AIRLINE_CODE, FLIGHT_NUMBER, DATE_FROM, DATE_TO)

    if arrival_info:
        logger.info(f"Fetched {len(arrival_info)} records from API")
        dump_data(arrival_info, OUTPUT_DIR, ARRIVAL_API_FILE_NAME)
    else:
        logger.warning("No data was returned from the API.")

    main_func_duration = round(time() - main_func_start_time, 2)
    logger.info(f"Flight arrival extraction completed in {main_func_duration} seconds")
    
if __name__ == "__main__":
    main()