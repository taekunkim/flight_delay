import os
import requests

from src.utils.logger import logger
from src.utils.helper import dump_data

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

API_KEY = os.getenv("FLIGHT_API_KEY")
API_BASE_URL = os.getenv("FLIGHT_API_BASE_URL")
DUMP_RAW_DATA = os.getenv("DUMP_RAW_DATA")

request_headers = {
        "Accept": "application/json",
        "Accept-Version": "v1",
        "Authorization": f"Bearer {API_KEY}"
    }

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
        flight_code: str,
        datetime_from: str,
        datetime_to: str,
        dump_file_name: str
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
    
    API_ENDPOINT = os.getenv("FLIGHT_ARRIVAL_API_ENDPOINT")

    logger.info(f"Preparing API request for flight arrival data")

    # set default values for datetime range
    if datetime_from == "":
        from datetime import datetime, timezone, timedelta
        current_datetime = datetime.now(timezone.utc)
        if datetime_to == "":
            fourteen_days_ago_datetime = current_datetime - timedelta(days=14)
        datetime_from = str(fourteen_days_ago_datetime).replace(" ", "T")[:-13] + "Z" 
        datetime_to = str(current_datetime).replace(" ", "T")[:-13] + "Z"

    query_params = {
        "flights": flight_code,
        "flight_datetime_from": datetime_from,
        "flight_datetime_to": datetime_to,
    }

    request_params = {
        "url": urljoin(API_BASE_URL, API_ENDPOINT),
        "params": query_params,
        "headers": request_headers,
    }

    try:
        logger.info(f"Fetching data from {request_params['url']}")
        response = requests.get(**request_params)
        response.raise_for_status()
        raw_data = response.json()
        logger.info(f"Finished fetching {len(raw_data):,} records of data.")
    
    except requests.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise e # raise error for retry
    
    # ───────────────────────────────
    # Dump raw data
    # ───────────────────────────────

    if DUMP_RAW_DATA:
        dump_filepath = urljoin(os.getenv("OUTPUT_DIR"), "flight_data", dump_file_name)
        dump_data(raw_data, dump_filepath)

    return raw_data
    