"""
Standard: Sovereign Architecture | Protocol: ERR_CODES_2026
Architect: Ali (Principal Architect)
Status: Self-Documenting Industrial Core.
"""


class DomainValidationError(Exception):
    """
    Sovereign Base Error.
    Action: Serves as the first line of defense in the Refinery.
    Logic: Enforces standardized error reporting across the domain.
    """

    def __init__(self, message: str, code: str):
        self.code = code
        self.message = message
        super().__init__(f"[{self.code}] {self.message}")


class PhysicalImpossibilityError(DomainValidationError):
    """
    Physical Law Violation.
    Action: Blocks data that contradicts NYC physical/legal transit limits.
    Default Code: ERR_DOM_VAL_011.
    """

    def __init__(self, message: str, code: str = "ERR_DOM_VAL_011"):
        super().__init__(message=message, code=code)


class FinancialMismatchError(DomainValidationError):
    """
    Accounting Integrity Violation.
    Action: Ensures sub-charges sum up to the total amount.
    Default Code: ERR_DOM_VAL_009.
    """

    def __init__(self, message: str, code: str = "ERR_DOM_VAL_009"):
        super().__init__(message=message, code=code)


class SpatialIntegrityError(DomainValidationError):
    """
    Spatial Protocol Violation.
    Action: Validates NYC Zone IDs and TLC Rate Codes.
    Default Code: ERR_DOM_VAL_007.
    """

    def __init__(self, message: str, code: str = "ERR_DOM_VAL_007"):
        super().__init__(message=message, code=code)


class TemporalAnomalyError(DomainValidationError):
    """
    Time Sequence Violation.
    Action: Prevents time-travel (dropoff before pickup).
    Default Code: ERR_DOM_VAL_012.
    """

    def __init__(self, message: str, code: str = "ERR_DOM_VAL_012"):
        super().__init__(message=message, code=code)
