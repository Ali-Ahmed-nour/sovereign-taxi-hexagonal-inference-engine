"""
MODULE: Quality Assurance - Sovereign 100% Path Exhaustion.
STANDARD: Sovereign Architecture (Zero External Dependencies).
ACTION: Absolute coverage for Entities and VOs with Strict Protocol Alignment.
ARCHITECT: Ali (Principal Architect).
"""

# 1. Standard Library Imports (Alphabetical)
import math
from datetime import datetime, timedelta
from unittest.mock import MagicMock

# 2. Third-Party Imports (Alphabetical)
import pytest

# 3. Local Application Imports (Alphabetical)
from src.core.domain.entities import TaxiTrip
from src.core.domain.exceptions import (
    DomainValidationError,
    FinancialMismatchError,
    PhysicalImpossibilityError,
    SpatialIntegrityError,
    TemporalAnomalyError,
)
from src.core.domain.value_objects import (
    TripFinancials,
    TripLocation,
    TripOccupancy,
    TripTemporal,
)
from tests.factories.trip_factory import (
    TaxiTripFactory,
    TripFinancialsFactory,
    TripLocationFactory,
    TripOccupancyFactory,
    TripTemporalFactory,
)

# Constant Protocol for Temporal Bins (NYC Standard)
MORNING_START, MORNING_END = 7, 9
EVENING_START, EVENING_END = 16, 19
NIGHT_START, NIGHT_END = 20, 5

# Constant Protocol for Spatial
VALID_ZONE_P = "ZONE_1"
VALID_ZONE_D = "ZONE_2"

# -------------------------------------------------------------------------
# 1. EXCEPTIONS: FULL SANCTUARY
# -------------------------------------------------------------------------


def test_exceptions_full_coverage_victory():
    """Action: Preserve the 100% coverage success in exceptions.py."""
    excs = [
        DomainValidationError("Base", "ERR_000"),
        PhysicalImpossibilityError("Speed Violation"),
        FinancialMismatchError("Audit Mismatch"),
        SpatialIntegrityError("Zone Protocol"),
        TemporalAnomalyError("Time Travel"),
    ]
    for err in excs:
        assert err.code.startswith("ERR_")  # noqa: S101
        assert isinstance(err, Exception)  # noqa: S101


# -------------------------------------------------------------------------
# 2. ENTITIES: EXHAUSTION
# -------------------------------------------------------------------------


def test_entity_integrity_exhaustion():
    """Action: Hit lines 67, 78, 93-96 (Financial Audit), 106 (Route Key)."""

    # Line 67: Trigger PhysicalImpossibilityError (Duration <= 0)
    mock_temporal = MagicMock(spec=TripTemporal)
    mock_temporal.duration_minutes = 0.0
    with pytest.raises(PhysicalImpossibilityError, match="ERR_DOM_VAL_013"):
        TaxiTrip(
            location=TripLocationFactory(pickup_id=VALID_ZONE_P, dropoff_id=VALID_ZONE_D),
            temporal=mock_temporal,
            financials=TripFinancialsFactory(),
            occupancy=TripOccupancyFactory(),
            source_id="DUR_FAIL",
        )

    # Line 78: Velocity limit (> 125 mph)
    t_start = datetime(2026, 1, 1, 12, 0)
    t_end = t_start + timedelta(seconds=1)
    fast_temp = TripTemporal(t_start, t_end)
    fast_occ = TripOccupancy(passenger_count=1, distance_miles=10.0)
    with pytest.raises(PhysicalImpossibilityError, match="ERR_DOM_VAL_001"):
        TaxiTrip(
            TripLocationFactory(pickup_id=VALID_ZONE_P, dropoff_id=VALID_ZONE_D),
            fast_temp,
            TripFinancialsFactory(),
            fast_occ,
            "SPEED",
        )

    # Lines 93-96: Financial Mismatch
    bad_fin = TripFinancialsFactory(fare_amount=10.0, tolls_amount=2.0)
    object.__setattr__(bad_fin, "total_amount", 99.0)
    with pytest.raises(FinancialMismatchError, match="ERR_DOM_VAL_002"):
        TaxiTrip(
            location=TripLocationFactory(pickup_id=VALID_ZONE_P, dropoff_id=VALID_ZONE_D),
            temporal=TripTemporalFactory(),
            financials=bad_fin,
            occupancy=TripOccupancyFactory(),
            source_id="FIN_FAIL",
        )

    # Line 106: route_key property trigger
    trip = TaxiTripFactory(location__pickup_id="ZONE_A", location__dropoff_id="ZONE_B")
    assert trip.route_key == "ZONE_A_TO_ZONE_B"  # noqa: S101


# -------------------------------------------------------------------------
# 3. VALUE OBJECTS: FULL PATH EXHAUSTION
# -------------------------------------------------------------------------


def test_vo_logic_exhaustion():
    """Action: Trigger all match branches and seasonal fallbacks."""

    # --- A. TripLocation: Branch Exhaustion ---
    with pytest.raises(SpatialIntegrityError, match="ERR_DOM_VAL_007"):
        TripLocation(pickup_id="WRONG_ID", dropoff_id="ZONE_A", rate_code="1")

    with pytest.raises(SpatialIntegrityError, match="ERR_DOM_VAL_008"):
        TripLocation(pickup_id="ZONE_A", dropoff_id="ZONE_B", rate_code="999")

    # Match Category Exhaustion
    loc_cases = [("2", "AIRPORT_JFK"), ("3", "NEWARK_OUT_OF_STATE"), ("1", "INTRA_ZONE_SHORT")]
    for code, expected in loc_cases:
        pickup = "ZONE_A"
        # لو الحالة INTRA_ZONE لازم المكانين يكونوا زي بعض عشان ندخل الـ Case صح
        dropoff = "ZONE_A" if expected == "INTRA_ZONE_SHORT" else "ZONE_B"
        assert TripLocation(pickup, dropoff, code).trip_category == expected  # noqa: S101

    for r in ["5", "6"]:
        assert TripLocation("ZONE_A", "ZONE_B", r).trip_category == "NEGOTIATED_OR_GROUP"  # noqa: S101

    # --- تغطية سطر 80: STANDARD_METRE_CITY (The Default Return) ---
    # نستخدم IDs مختلفة و Rate Code 1 عشان نتخطى كل الـ cases ونوصل لآخر سطر
    standard_trip = TripLocation("ZONE_X", "ZONE_Y", "1")
    assert standard_trip.trip_category == "STANDARD_METRE_CITY"  # noqa: S101

    # --- B. TripOccupancy: Atomic Defense ---
    with pytest.raises(PhysicalImpossibilityError, match="ERR_DOM_VAL_010"):
        TripOccupancy(passenger_count=0, distance_miles=1.0)
    with pytest.raises(PhysicalImpossibilityError, match="ERR_DOM_VAL_011"):
        TripOccupancy(passenger_count=1, distance_miles=600.0)

    # --- C. TripTemporal: Temporal Path Exhaustion ---

    # --- تغطية سطر 194: Temporal Anomaly (Time Travel) ---
    # نختبر حالة الـ <= بالظبط (الوصول قبل الركوب)
    with pytest.raises(TemporalAnomalyError, match="ERR_DOM_VAL_012"):
        TripTemporal(pickup_at=datetime(2026, 1, 1, 12, 0), dropoff_at=datetime(2026, 1, 1, 11, 59))

    # نختبر حالة التساوي (Boundary)
    with pytest.raises(TemporalAnomalyError, match="ERR_DOM_VAL_012"):
        TripTemporal(pickup_at=datetime(2026, 1, 1, 12, 0), dropoff_at=datetime(2026, 1, 1, 12, 0))

    # بقية الـ Bins (Morning, Evening, Night, Off-Peak)
    time_tests = [
        (8, "MORNING_RUSH"),
        (17, "EVENING_RUSH"),
        (23, "NIGHT"),
        (2, "NIGHT"),
        (12, "OFF_PEAK"),
    ]
    for hour, expected in time_tests:
        t_temp = TripTemporal(datetime(2026, 1, 1, hour, 0), datetime(2026, 1, 1, hour, 30))
        assert t_temp.time_of_day_bin == expected  # noqa: S101

    # Seasonal Fallback (October -> AUTUMN)
    t_season = TripTemporal(datetime(2026, 10, 1), datetime(2026, 10, 1, 1))
    assert t_season.seasonal_context == "AUTUMN"  # noqa: S101

    # Cyclical Signals & Duration Math
    t_math = TripTemporal(datetime(2026, 1, 1, 12, 0), datetime(2026, 1, 1, 13, 0))
    signals = t_math.cyclical_signals
    expected_norm = 2 * math.pi * (12 * 3600) / 86400
    assert signals["sin"] == pytest.approx(math.sin(expected_norm), abs=1e-9)  # noqa: S101
    assert t_math.duration_minutes == pytest.approx(60.0, abs=1e-6)  # noqa: S101


# -------------------------------------------------------------------------
# 4. FINANCIALS: THE MISSING LINKS EXHAUSTION
# -------------------------------------------------------------------------


def test_financials_logic_exhaustion():
    """Action: Achieve 100% coverage for TripFinancials."""

    # 1. Negative Flow Audit
    with pytest.raises(FinancialMismatchError, match="fare_amount cannot be negative"):
        TripFinancials(
            fare_amount=-5.0,
            extra=0.0,
            mta_tax=0.0,
            tip_amount=0.0,
            tolls_amount=0.0,
            improvement_surcharge=0.0,
            congestion_surcharge=0.0,
            airport_fee=0.0,
            cbd_congestion_fee=0.0,
            total_amount=-5.0,
        )

    # 2. Sum Mismatch
    with pytest.raises(FinancialMismatchError, match="Accounting mismatch"):
        TripFinancials(
            fare_amount=10.0,
            extra=2.0,
            mta_tax=0.5,
            tip_amount=1.0,
            tolls_amount=0.0,
            improvement_surcharge=0.0,
            congestion_surcharge=0.0,
            airport_fee=0.0,
            cbd_congestion_fee=0.0,
            total_amount=20.0,
        )

    # 3. Property Calculation
    valid_fin = TripFinancialsFactory(fare_amount=20.0)
    from dataclasses import replace

    # Using replace to ensure frozen dataclass total matches calculated
    valid_fin = replace(valid_fin, total_amount=valid_fin.calculated_total)
    assert valid_fin.calculated_total > 0  # noqa: S101
