from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FlightArrival(Base):
    __tablename__ = "flight_arrivals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    airline_iata_code = Column(String(2))
    flight_number = Column(String(10))
    scheduled_time = Column(TIMESTAMP)
    actual_arrival = Column(TIMESTAMP)
    departure_delay = Column(Integer)
    ingested_at = Column(TIMESTAMP)
