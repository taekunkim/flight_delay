from sqlalchemy import Column, String, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.sql import func
from src.db.database import Base

class FlightDelay(Base):
    __tablename__ = "flight_delay"

    flight_cd = Column(String(8))
    takeoff_dtm = Column(TIMESTAMP(timezone=True))
    landing_dtm = Column(TIMESTAMP(timezone=True))
    ingested_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("flight_cd", "takeoff_dtm"),
    )