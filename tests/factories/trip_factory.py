"""
MODULE: Quality Assurance - Sovereign Trip Factory.
STANDARD: Factory-Boy (Sub-module Explicit Imports).
PROTOCOL: Self-Documenting Domain Language (SDDL).
ARCHITECT: Ali (Principal Architect).
ACTION: Synthesizes high-fidelity TaxiTrip aggregates for industrial validation.
"""

from datetime import datetime, timedelta

# Rationale: Explicit sub-module imports to satisfy Pylance/Pyright strict mode.
from factory.base import Factory
from factory.declarations import LazyAttribute, LazyFunction, Sequence, SubFactory

# Rationale: Direct import from Domain Sanctuary to ensure type-safe instantiation.
from src.core.domain.entities import TaxiTrip
from src.core.domain.value_objects import (
    TripFinancials,
    TripLocation,
    TripOccupancy,
    TripTemporal,
)


class TripLocationFactory(Factory):
    """
    Action: Generates spatial context for trips.
    Logic: Uses sequences to ensure pickup and dropoff zones are distinct and incremental.
    Rationale: Prevents data collisions in spatial indexing during batch tests.
    """

    class Meta:
        model = TripLocation

    pickup_id = Sequence(lambda n: f"ZONE_{n:03d}")
    dropoff_id = Sequence(lambda n: f"ZONE_{(n + 1):03d}")
    rate_code = "1"


class TripTemporalFactory(Factory):
    """
    Action: Manages temporal data sequence.
    Logic: Calculates dropoff time based on a fixed 15-minute offset from pickup.
    Rationale: Guarantees a positive non-zero duration to satisfy Domain Invariants.
    """

    class Meta:
        model = TripTemporal

    pickup_at = LazyFunction(datetime.now)
    dropoff_at = LazyAttribute(lambda o: o.pickup_at + timedelta(minutes=15))


class TripFinancialsFactory(Factory):
    class Meta:
        model = TripFinancials

    fare_amount = 20.0
    extra = 0.5
    mta_tax = 0.5
    tip_amount = 5.0
    tolls_amount = 0.0
    improvement_surcharge = 0.3
    congestion_surcharge = 0.0
    airport_fee = 0.0
    cbd_congestion_fee = 0.0

    # Rationale: Dynamic calculation ensures ERR_DOM_VAL_009 is not triggered
    # unless we explicitly want it for financial testing.
    total_amount = LazyAttribute(
        lambda o: sum(
            [
                o.fare_amount,
                o.extra,
                o.mta_tax,
                o.tip_amount,
                o.tolls_amount,
                o.improvement_surcharge,
                o.congestion_surcharge,
                o.airport_fee,
                o.cbd_congestion_fee,
            ]
        )
    )


class TripOccupancyFactory(Factory):
    """
    Action: Defines physical occupancy and distance.
    Logic: Sets baseline passenger count and transit distance.
    Rationale: Provides stable values for velocity and pricing calculations.
    """

    class Meta:
        model = TripOccupancy

    passenger_count = 1
    distance_miles = 5.0  # Unified naming to miles per protocol


class TaxiTripFactory(Factory):
    """
    Action: Orchestrates the construction of a Sovereign TaxiTrip.
    Logic: Nests specialized factories into a single aggregate root.
    Rationale: Centralizes synthetic data creation for the Sovereign Quality Suite.
    """

    class Meta:
        model = TaxiTrip

    location = SubFactory(TripLocationFactory)
    temporal = SubFactory(TripTemporalFactory)
    financials = SubFactory(TripFinancialsFactory)
    occupancy = SubFactory(TripOccupancyFactory)

    source_id = Sequence(lambda n: f"NYC_TX_{n:04d}")

    # Registry Pattern: ML predictions container
    predictions = LazyFunction(dict)


# --- SDDL Audit ---
# Action: TaxiTripFactory provides a clean API for test data.
# Logic: trip = TaxiTripFactory(occupancy__distance_miles=10.0)
# Rationale: Minimizes boilerplate while maintaining strict Domain Core integrity.
