"""Socratic Conflict - Conflict detection and resolution system."""

from socratic_conflict.async_detector import AsyncConflictDetector
from socratic_conflict.consensus.algorithms import (
    ConsensusAlgorithm,
    MajorityConsensus,
    QuorumConsensus,
    RankedChoiceConsensus,
    SupermajorityConsensus,
    UnanimousConsensus,
)
from socratic_conflict.core.conflict import (
    Conflict,
    ConflictDecision,
    Proposal,
    Resolution,
)
from socratic_conflict.detection.detector import ConflictDetector
from socratic_conflict.exceptions import (
    ConflictDetectionError,
    ConflictDetectionException,
    ConflictValidationException,
    ConsensusAlgorithmError,
    ConsensusException,
    ConsensusTimeoutError,
    HistoryException,
    HistoryNotFoundError,
    HistoryTrackingError,
    InsufficientQuorumError,
    IntegrationException,
    InvalidAgentError,
    InvalidContextError,
    InvalidConflictDataError,
    InvalidProposalError,
    InvalidResolutionStateError,
    NoResolutionFoundError,
    ProposalException,
    ProposalValidationError,
    ResolutionException,
    ResolutionStrategyError,
    ResolutionValidationError,
    SocraticConflictException,
    SkillIntegrationError,
    ToolIntegrationError,
)
from socratic_conflict.history.tracker import HistoryTracker
from socratic_conflict.integrations.langchain import ConflictResolutionTool
from socratic_conflict.integrations.openclaw import SocraticConflictSkill
from socratic_conflict.resolution.strategies import (
    ConsensusStrategy,
    HybridStrategy,
    PriorityStrategy,
    ResolutionStrategy,
    VotingStrategy,
    WeightedStrategy,
)

__version__ = "0.1.2"

__all__ = [
    # Core models
    "Conflict",
    "ConflictDecision",
    "Proposal",
    "Resolution",
    # Detection
    "ConflictDetector",
    "AsyncConflictDetector",
    # Resolution strategies
    "ResolutionStrategy",
    "VotingStrategy",
    "ConsensusStrategy",
    "WeightedStrategy",
    "PriorityStrategy",
    "HybridStrategy",
    # Consensus algorithms
    "ConsensusAlgorithm",
    "MajorityConsensus",
    "UnanimousConsensus",
    "SupermajorityConsensus",
    "RankedChoiceConsensus",
    "QuorumConsensus",
    # History tracking
    "HistoryTracker",
    # Framework integrations
    "SocraticConflictSkill",
    "ConflictResolutionTool",
    # Exceptions
    "SocraticConflictException",
    "ConflictDetectionException",
    "ConflictDetectionError",
    "InvalidConflictDataError",
    "ProposalException",
    "InvalidProposalError",
    "ProposalValidationError",
    "ConsensusException",
    "ConsensusAlgorithmError",
    "InsufficientQuorumError",
    "ConsensusTimeoutError",
    "ResolutionException",
    "ResolutionStrategyError",
    "NoResolutionFoundError",
    "ResolutionValidationError",
    "InvalidResolutionStateError",
    "HistoryException",
    "HistoryTrackingError",
    "HistoryNotFoundError",
    "ConflictValidationException",
    "InvalidAgentError",
    "InvalidContextError",
    "IntegrationException",
    "ToolIntegrationError",
    "SkillIntegrationError",
]
