from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Location:
    """Value Object for taxi locations."""

    location_id: str


@dataclass(frozen=True)
class TaxiTrip:
    """Core Domain Entity representing a single taxi trip."""

    trip_id: str
    pickup_loc: Location
    dropoff_loc: Location
    pickup_time: datetime
    dropoff_time: datetime

    @property
    def duration(self) -> float:
        """Calculate duration in minutes."""
        # Using timedelta to get total minutes
        delta = self.dropoff_time - self.pickup_time
        return delta.total_seconds() / 60

    def is_valid_for_model(self) -> bool:
        """Business Rule: Trip must be between 1 and 60 minutes."""
        return 1 <= self.duration <= 60
