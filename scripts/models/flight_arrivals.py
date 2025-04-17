from sqlalchemy import Column, Integer, String, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class FlightArrival(Base):
    __tablename__ = "flight_arrivals"

    airline_iata_code = Column(String(2), nullable=False)
    flight_number = Column(String(10), nullable=False)
    scheduled_arrival = Column(TIMESTAMP, nullable=False)       

    actual_arrival = Column(TIMESTAMP)
    departure_delay = Column(Integer)
    ingested_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("airline_iata_code", "flight_number", "scheduled_arrival"),
    )