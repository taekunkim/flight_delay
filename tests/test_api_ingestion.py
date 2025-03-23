
import pytest
from unittest.mock import patch, MagicMock
from scripts.extract_flight_arrival_data import get_arrival_info

# Sample API response based on the user's data
sample_response = [
    {
        "type": "arrival",
        "status": "landed",
        "departure": {
            "iataCode": "ist",
            "icaoCode": "ltfm",
            "gate": "d14",
            "delay": 25,
            "scheduledTime": "2025-02-28t17:10:00.000",
            "estimatedTime": "2025-02-28t17:00:00.000",
            "actualTime": "2025-02-28t17:34:00.000",
            "estimatedRunway": "2025-02-28t17:34:00.000",
            "actualRunway": "2025-02-28t17:34:00.000"
        },
        "arrival": {
            "iataCode": "icn",
            "icaoCode": "rksi",
            "terminal": "1",
            "baggage": "18",
            "gate": "40",
            "scheduledTime": "2025-03-01t09:05:00.000",
            "estimatedTime": "2025-03-01t08:48:00.000",
            "actualTime": "2025-03-01t08:51:00.000",
            "estimatedRunway": "2025-03-01t08:51:00.000",
            "actualRunway": "2025-03-01t08:51:00.000"
        },
        "airline": {
            "name": "asiana airlines",
            "iataCode": "oz",
            "icaoCode": "aar"
        },
        "flight": {
            "number": "6934",
            "iataNumber": "oz6934",
            "icaoNumber": "aar6934"
        },
        "codeshared": {
            "airline": {
                "name": "turkish airlines",
                "iataCode": "tk",
                "icaoCode": "thy"
            },
            "flight": {
                "number": "20",
                "iataNumber": "tk20",
                "icaoNumber": "thy20"
            }
        }
    }
]

@patch("scripts.extract_flight_arrival_data.requests.get")
def test_get_arrival_info_returns_sample_data(mock_get):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    result = get_arrival_info(
        api_key="FAKE_KEY",
        arrival_airport="ICN",
        airline_code="OZ",
        flight_number="6934",
        start_date_str="2025-02-28",
        end_date_str="2025-03-01"
    )

    # Assert
    assert isinstance(result, list)
    assert result == sample_response
    assert result[0]["arrival"]["iataCode"] == "icn"
    assert result[0]["airline"]["name"] == "asiana airlines"
    mock_get.assert_called_once()
