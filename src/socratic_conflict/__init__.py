"""Socratic Conflict - Conflict detection and resolution system."""

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
from socratic_conflict.history.tracker import HistoryTracker
from socratic_conflict.resolution.strategies import (
    ConsensusStrategy,
    HybridStrategy,
    PriorityStrategy,
    ResolutionStrategy,
    VotingStrategy,
    WeightedStrategy,
)

__all__ = [
    # Core models
    "Conflict",
    "ConflictDecision",
    "Proposal",
    "Resolution",
    # Detection
    "ConflictDetector",
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
]
