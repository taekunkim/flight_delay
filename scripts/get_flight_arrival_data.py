import os
import requests

from scripts.logger import logger
from scripts.utils import dump_data
from scripts.models.flight_arrivals import FlightArrival

from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urljoin, urlencode
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

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
DUMP_DATA = os.getenv("DUMP_DATA")

# ───────────────────────────────
# API Function
# ───────────────────────────────
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff: 2s, 4s, 8s...
    stop=stop_after_attempt(3),                          # Retry up to 3 times
    retry=retry_if_exception_type(requests.RequestException),  # Retry only on request errors
    reraise=True,  # Raise final exception if all retries fail
    # before_sleep=logger,  # Log each retry attempt
    # after=logger.info("Retry attempt complete.")  # Optional hook
)
def get_flight_arrival_data(
        api_key: str, 
        arrival_airport: str, 
        airline_code: str, 
        flight_number: str, 
        start_date_str: str, 
        end_date_str: str
    ) -> list[dict]:
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
    

    # ───────────────────────────────
    # Load raw data
    # ───────────────────────────────

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
        logger.info(f"Fetching data from {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info(f"API call successful, status code {response.status_code}")
        raw_data = response.json()
        logger.info(f"Finished fetching {len(raw_data)} records of data.")
    
    except requests.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise # raise error for retry

    # ───────────────────────────────
    # Dump raw data
    # ───────────────────────────────

    if DUMP_DATA:
        OUTPUT_DIR = os.getenv("OUTPUT_DIR")
        ARRIVAL_API_FILE_NAME = os.getenv("ARRIVAL_API_FILE_NAME")

        logger.info(f"Dumping raw data to {OUTPUT_DIR}/{ARRIVAL_API_FILE_NAME}")
        dump_data(raw_data, OUTPUT_DIR, ARRIVAL_API_FILE_NAME)

    # ───────────────────────────────
    # Prepare data for SQLAlchemy
    # ───────────────────────────────
        
    logger.info("Transforming data for SQLAlchemy")

    clean_data = []
    skip_counter = 0 # number of records skipped while parsing
    for each in raw_data:
        try:
            clean_each = {
                "airline_iata_code": each.get("airline").get("iataCode"),
                "flight_number": each.get("flight").get("number"),
                "scheduled_arrival": datetime.fromisoformat(each.get("arrival").get("scheduledTime").replace("t", "T")),
                "actual_arrival": datetime.fromisoformat(each.get("arrival").get("actualTime").replace("t", "T")),
                "departure_delay": each.get("departure").get("delay"),
            }
            clean_data.append(clean_each)

        except Exception as e:
            skip_counter += 1
        
    logger.warning(f"Skipped parsing {skip_counter} records due to invalid data.")

    logger.info("Finished transforming data for SQLAlchemy")

    return clean_data
    