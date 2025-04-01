from .flight_arrivals import FlightArrival
from .flight_arrivals import Base  # ✅ the shared Base used by all models

__all__ = ["FlightArrival", "Base"]