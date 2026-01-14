"""
Entities Module - Domain Core Layer.
Standard: Sovereign Architecture (Zero External Dependencies).
Protocol: Hexagonal / DDD Sovereign Sanctuary.
Architect: Ali (Principal Architect)
Status: Industrial SOTA (Atomic Validation & Educational Rationale).
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .exceptions import FinancialMismatchError, PhysicalImpossibilityError

# Import from local sanctuary brothers
from .value_objects import TripFinancials, TripLocation, TripOccupancy, TripTemporal

# --- Sovereign Domain Constants ---
# Rationale: 125 mph is the hard physical ceiling for urban transit safety in NYC.
MAX_ALLOWED_VELOCITY_MPH = 125.0
# Rationale: Float precision guard (1 cent) to ensure accounting integrity.
CURRENCY_TOLERANCE_THRESHOLD = 0.01


@dataclass(frozen=True, slots=True)
class TaxiTrip:
    """
    Sovereign Aggregate Root: TaxiTrip.
    Responsibility: Orchestrate trip data and enforce cross-object invariants.

    Invariants:
    - Velocity: Maximum allowable city transit speed is 125 mph.
    - Temporal: Trip duration must be positive non-zero.
    - Financial: Total amount must align with the sum of all sub-charges.
    """

    # 1. State Composition (Immutable Value Objects)
    location: TripLocation
    temporal: TripTemporal
    financials: TripFinancials
    occupancy: TripOccupancy

    # 2. Identity & Registry (Sovereign Metadata)
    source_id: str  # Original ID from NYC TLC Source (Traceability).
    trip_id: UUID = field(default_factory=uuid4)
    # Registry Pattern for ML Model Predictions: Stores model_name -> prediction_value.
    predictions: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """
        Action: Triggers the Atomic Integrity Guard sequence.
        Rationale: Ensures the entity never exists in an invalid state without intermediaries.
        Logic: Direct execution of check-methods to enforce Sovereign boundaries.
        """
        self._check_physical_velocity()
        self._check_financial_integrity()

    def _check_physical_velocity(self):
        """
        Physics Engine: Enforces Newton's Laws and urban safety limits.
        Action: Detects sensor malfunctions or impossible transit speeds.
        Logic: Compares duration vs distance using Miles per Hour (MPH).
        Rationale: NYC traffic physics dictating that no legal trip exceeds 125 mph.
        """
        # Duration Check: Temporal Invariant.
        if self.temporal.duration_minutes <= 0:
            raise PhysicalImpossibilityError(
                message="ERR_DOM_VAL_013: Non-positive duration. Time-travel blocked.",
                code="ERR_DOM_VAL_013",
            )

        # Velocity Calculation (Miles / Hours)
        duration_hr = self.temporal.duration_minutes / 60.0
        velocity_mph = self.occupancy.distance_miles / duration_hr

        # Physical Boundary Enforcement (125 mph)
        if velocity_mph > MAX_ALLOWED_VELOCITY_MPH:
            raise PhysicalImpossibilityError(
                message=f"ERR_DOM_VAL_001: Velocity {velocity_mph:.2f} mph exceeds NYC limit."
            )

    def _check_financial_integrity(self):
        """
        Financial Audit: Ensures arithmetic consistency across sub-charges.
        Action: Protects the system from ghost charges and data corruption.
        Logic: sum(components) == total_amount within 1 cent tolerance.
        Rationale: Guards against floating-point errors and financial fraud.
        """
        calculated = self.financials.calculated_total
        actual = self.financials.total_amount

        if abs(actual - calculated) > CURRENCY_TOLERANCE_THRESHOLD:
            error_msg = (
                f"ERR_DOM_VAL_002: Total ({actual}) mismatches calculated sum ({calculated})."
            )
            raise FinancialMismatchError(message=error_msg)

    @property
    def route_key(self) -> str:
        """
        Feature Engineering (SOTA): Optimized Route Identifier.
        Action: Pre-computes and caches the spatial relation for ML indexing.
        Logic: Concatenates pickup and dropoff IDs.
        Rationale: Calculated once per entity lifetime to save compute cycles.
        """
        return f"{self.location.pickup_id}_TO_{self.location.dropoff_id}"
