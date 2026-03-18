"""Exception hierarchy for Socratic Conflict.

Provides domain-specific exceptions for conflict detection and resolution,
organized by functional area for better error handling and debugging.
"""


class SocraticConflictException(Exception):
    """Base exception for all Socratic Conflict errors."""

    pass


# Conflict detection exceptions


class ConflictDetectionException(SocraticConflictException):
    """Base exception for conflict detection failures."""

    pass


class ConflictDetectionError(ConflictDetectionException):
    """Raised when conflict detection fails."""

    pass


class InvalidConflictDataError(ConflictDetectionException):
    """Raised when conflict data is invalid or malformed."""

    pass


# Proposal exceptions


class ProposalException(SocraticConflictException):
    """Base exception for proposal-related errors."""

    pass


class InvalidProposalError(ProposalException):
    """Raised when proposal data is invalid."""

    pass


class ProposalValidationError(ProposalException):
    """Raised when proposal validation fails."""

    pass


# Consensus exceptions


class ConsensusException(SocraticConflictException):
    """Base exception for consensus operation failures."""

    pass


class ConsensusAlgorithmError(ConsensusException):
    """Raised when consensus algorithm execution fails."""

    pass


class InsufficientQuorumError(ConsensusException):
    """Raised when consensus cannot be reached due to insufficient agreement.

    This occurs when:
    - Vote count is below required threshold
    - Agreement percentage is below required consensus level
    - Not enough participants to form quorum
    """

    pass


class ConsensusTimeoutError(ConsensusException):
    """Raised when consensus operation times out."""

    pass


# Resolution exceptions


class ResolutionException(SocraticConflictException):
    """Base exception for conflict resolution failures."""

    pass


class ResolutionStrategyError(ResolutionException):
    """Raised when a resolution strategy fails to resolve a conflict."""

    pass


class NoResolutionFoundError(ResolutionException):
    """Raised when no resolution can be found for a conflict."""

    pass


class ResolutionValidationError(ResolutionException):
    """Raised when resolution data fails validation."""

    pass


class InvalidResolutionStateError(ResolutionException):
    """Raised when a resolution operation violates resolution state."""

    pass


# History and tracking exceptions


class HistoryException(SocraticConflictException):
    """Base exception for conflict history tracking failures."""

    pass


class HistoryTrackingError(HistoryException):
    """Raised when conflict history recording fails."""

    pass


class HistoryNotFoundError(HistoryException):
    """Raised when requested history cannot be found."""

    pass


# Data validation exceptions


class ConflictValidationException(SocraticConflictException):
    """Base exception for conflict validation failures."""

    pass


class InvalidAgentError(ConflictValidationException):
    """Raised when an agent is invalid or missing."""

    pass


class InvalidContextError(ConflictValidationException):
    """Raised when conflict context is invalid."""

    pass


# Integration exceptions


class IntegrationException(SocraticConflictException):
    """Base exception for framework integration errors."""

    pass


class ToolIntegrationError(IntegrationException):
    """Raised when framework tool integration fails."""

    pass


class SkillIntegrationError(IntegrationException):
    """Raised when framework skill integration fails."""

    pass
