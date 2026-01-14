"""
MODULE: Value Objects - Domain Core Layer.
STANDARD: Sovereign Architecture (Zero External Dependencies).
CONTEXT: NYC Taxi Duration Prediction System (Industrial SOTA).
STATUS: Ruff-Verified & Self-Documenting.
PRINCIPAL ARCHITECT: Ali
"""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .exceptions import (
    FinancialMismatchError,
    PhysicalImpossibilityError,
    SpatialIntegrityError,
    TemporalAnomalyError,
)

# --- Domain Constants ---
ZONE_PREFIX = "ZONE_"
MAX_PASSENGER_LIMIT = 9
MAX_DISTANCE_MILES = 500.0
OFFICIAL_RATE_CODES = {"1", "2", "3", "4", "5", "6", "99"}

MORNING_START, MORNING_END = 7, 10
EVENING_START, EVENING_END = 16, 20
NIGHT_START, NIGHT_END = 23, 5


@dataclass(frozen=True, slots=True)
class TripLocation:
    """
    Spatial Value Object.
    Responsibility: Manage location identifiers and taxi rate protocols.
    """

    pickup_id: str
    dropoff_id: str
    rate_code: str

    def __post_init__(self):
        """Action: Execute integrity checks during object creation."""
        self._check_integrity()

    def _check_integrity(self):
        """Action: Validate prefix protocol and TLC rate code legitimacy."""
        is_valid_prefix = self.pickup_id.startswith(ZONE_PREFIX) and self.dropoff_id.startswith(
            ZONE_PREFIX
        )
        if not is_valid_prefix:
            raise SpatialIntegrityError(f"IDs must use {ZONE_PREFIX} protocol.", "ERR_DOM_VAL_007")

        if self.rate_code not in OFFICIAL_RATE_CODES:
            raise SpatialIntegrityError(
                f"Invalid NYC TLC RateCode: {self.rate_code}", "ERR_DOM_VAL_008"
            )

    @property
    def trip_category(self) -> str:
        """
        Action: Categorize trips into industrial segments for ML feature engineering.
        Logic: Executes structural pattern matching on TLC rate codes and spatial identifiers.
        Rationale: Centralizes classification logic within the Domain Core to ensure feature
                   consistency between training and inference, while complying with FURB126
                   by using a non-conditional fallback return.
        """
        match (self.rate_code, self.pickup_id, self.dropoff_id):
            case ("2", _, _):
                return "AIRPORT_JFK"
            case ("3", _, _):
                return "NEWARK_OUT_OF_STATE"
            case (_, p, d) if p == d:
                return "INTRA_ZONE_SHORT"
            case ("5" | "6", _, _):
                return "NEGOTIATED_OR_GROUP"

        # Action: Fallback for all standard city missions.
        return "STANDARD_METRE_CITY"


@dataclass(frozen=True, slots=True)
class TripFinancials:
    """
    Financial Integrity Engine.
    Responsibility: Audit financial records and ensure mathematical consistency.
    """

    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    improvement_surcharge: float
    congestion_surcharge: float
    airport_fee: float
    cbd_congestion_fee: float
    total_amount: float

    def __post_init__(self):
        """
        Action: Protect against negative financial flows and accounting mismatches.
        Logic: Sequentially executes positive flow audit and accounting integrity verification.
        Rationale: Multi-stage validation ensures that the object state is physically and
        mathematically immutable from the moment of inception.
        """
        self._check_positive_flow()
        self._check_accounting_integrity()

    def _check_positive_flow(self):
        """
        Action: Ensure critical financial fields are non-negative.
        Logic: Iterates through core financial attributes using reflection (getattr).
        Rationale: Negative fares or tips are logically impossible in a standard taxi transaction.
        """
        for field_name in ("fare_amount", "tip_amount", "total_amount"):
            if getattr(self, field_name) < 0:
                raise FinancialMismatchError(f"{field_name} cannot be negative.", "ERR_DOM_VAL_009")

    def _check_accounting_integrity(self):
        """
        Action: Verify that total_amount matches the sum of all components.
        Logic: Uses math.isclose to compare total_amount with calculated_total.
        Rationale: Prevents financial leakage and fraud. A tolerance of 0.01 (1 cent)
                   is permitted to account for standard floating-point precision issues.
        """
        if not math.isclose(self.total_amount, self.calculated_total, abs_tol=0.01):
            raise FinancialMismatchError(
                f"Accounting mismatch: total {self.total_amount} != sum {self.calculated_total}",
                "ERR_DOM_VAL_009",
            )

    @property
    def calculated_total(self) -> float:
        """
        Action: Audit and sum all surcharge components.
        Logic: Aggregates financial fields into a single fiscal sum using a tuple.
        Rationale: Tuples are used over lists for fixed-size sets to optimize memory
                   and satisfy industrial performance standards.
        """
        return sum(
            (
                self.fare_amount,
                self.extra,
                self.mta_tax,
                self.tip_amount,
                self.tolls_amount,
                self.improvement_surcharge,
                self.congestion_surcharge,
                self.airport_fee,
                self.cbd_congestion_fee,
            )
        )


@dataclass(frozen=True, slots=True)
class TripOccupancy:
    """
    Physical Trip Dimensions.
    Responsibility: Guard against physically impossible passenger counts or distances.
    """

    passenger_count: int
    distance_miles: float

    def __post_init__(self):
        """Action: Enforce NYC safety and physical boundaries."""
        if not (0 < self.passenger_count <= MAX_PASSENGER_LIMIT):
            raise PhysicalImpossibilityError(
                "Passenger count violates safety limits.", "ERR_DOM_VAL_010"
            )
        if not (0 < self.distance_miles <= MAX_DISTANCE_MILES):
            raise PhysicalImpossibilityError(
                "Distance exceeds physical boundaries.", "ERR_DOM_VAL_011"
            )


@dataclass(frozen=True, slots=True)
class TripTemporal:
    """
    High-Frequency Temporal Engine.
    Responsibility: Transform raw timestamps into ML-ready cyclical features.
    """

    pickup_at: datetime
    dropoff_at: datetime
    is_holiday: bool = False
    event_name: str = "NONE"

    def __post_init__(self):
        """Action: Prevent temporal anomalies (time-travel)."""
        if self.dropoff_at <= self.pickup_at:
            raise TemporalAnomalyError(
                "Temporal anomaly. Dropoff before pickup.", "ERR_DOM_VAL_012"
            )

    @property
    def duration_minutes(self) -> float:
        """Logic: Calculate primary target variable for prediction."""
        return (self.dropoff_at - self.pickup_at).total_seconds() / 60.0

    @property
    def time_of_day_bin(self) -> Literal["MORNING_RUSH", "EVENING_RUSH", "NIGHT", "OFF_PEAK"]:
        """Logic: Categorize hours into NYC operational traffic bins."""
        match self.pickup_at.hour:
            case h if MORNING_START <= h <= MORNING_END:
                return "MORNING_RUSH"
            case h if EVENING_START <= h <= EVENING_END:
                return "EVENING_RUSH"
            case h if h >= NIGHT_START or h <= NIGHT_END:
                return "NIGHT"

        return "OFF_PEAK"

    @property
    def seasonal_context(self) -> str:
        """Logic: Map pickup month to industrial season."""
        return {
            12: "WINTER",
            1: "WINTER",
            2: "WINTER",
            3: "SPRING",
            4: "SPRING",
            5: "SPRING",
            6: "SUMMER",
            7: "SUMMER",
            8: "SUMMER",
        }.get(self.pickup_at.month, "AUTUMN")

    @property
    def cyclical_signals(self) -> dict[str, float]:
        """
        Logic: Convert time into Sine/Cosine waves for periodicity.
        Rationale: Allows the model to understand the continuity of 24h cycles.
        """
        seconds = self.pickup_at.hour * 3600 + self.pickup_at.minute * 60 + self.pickup_at.second
        norm = 2 * math.pi * seconds / 86400
        return {"sin": math.sin(norm), "cos": math.cos(norm)}
