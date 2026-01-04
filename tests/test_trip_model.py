import pytest
from datetime import datetime

# Directly importing from the model file
from src.core.domain.model import TaxiTrip, Location


def test_taxi_trip_duration_calculation():
    # Arrange: Setup initial data
    pickup = datetime(2025, 10, 1, 10, 0, 0)
    dropoff = datetime(2025, 10, 1, 10, 15, 0)  # 15 minutes difference

    trip = TaxiTrip(
        trip_id="test-123",
        pickup_loc=Location("A"),
        dropoff_loc=Location("B"),
        pickup_time=pickup,
        dropoff_time=dropoff,
    )

    # Act: Execute the logic
    duration = trip.duration

    # Assert: Fixed floating point check with pytest.approx
    assert duration == pytest.approx(15.0)


def test_taxi_trip_validation():
    # Arrange: Setup an invalid trip (duration < 1 minute)
    pickup = datetime(2025, 10, 1, 10, 0, 0)
    dropoff = datetime(2025, 10, 1, 10, 0, 30)  # 30 seconds only

    trip = TaxiTrip(
        trip_id="test-invalid",
        pickup_loc=Location("A"),
        dropoff_loc=Location("B"),
        pickup_time=pickup,
        dropoff_time=dropoff,
    )

    # Assert: Business rule should fail
    assert trip.is_valid_for_model() is False
