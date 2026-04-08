"""Consensus algorithms for reaching agreements between agents."""

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from socratic_conflict.core.conflict import Proposal


class ConsensusAlgorithm:
    """Base class for consensus algorithms."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus on a set of proposals.

        Args:
            proposals: List of proposals to find consensus on

        Returns:
            Chosen Proposal with consensus or None
        """
        raise NotImplementedError


class MajorityConsensus(ConsensusAlgorithm):
    """Majority consensus - returns proposal with highest support."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus by selecting proposal with highest confidence.

        Args:
            proposals: List of proposals

        Returns:
            Proposal with highest confidence
        """
        if not proposals:
            return None

        # Return proposal with highest confidence
        return max(proposals, key=lambda p: p.confidence)


class UnanimousConsensus(ConsensusAlgorithm):
    """Unanimous consensus - requires unanimous support (confidence = 1.0)."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via unanimity.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal if it has unanimous support (confidence = 1.0), or None
        """
        if not proposals:
            return None

        # Find proposal with highest confidence
        best_proposal = max(proposals, key=lambda p: p.confidence)

        # Return only if it has unanimous support (perfect confidence)
        if best_proposal.confidence == 1.0:
            return best_proposal

        return None


class SupermajorityConsensus(ConsensusAlgorithm):
    """Supermajority consensus - requires support above configured threshold."""

    def __init__(self, threshold: float = 2.0 / 3.0):
        """Initialize with threshold.

        Args:
            threshold: Required confidence fraction (e.g., 0.67 for 2/3)
        """
        self.threshold = threshold

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via supermajority.

        Args:
            proposals: List of proposals

        Returns:
            Proposal with confidence above threshold, or None
        """
        if not proposals:
            return None

        # Find proposal with highest confidence
        best_proposal = max(proposals, key=lambda p: p.confidence)

        # Return if it meets the supermajority threshold
        if best_proposal.confidence >= self.threshold:
            return best_proposal

        return None


class RankedChoiceConsensus(ConsensusAlgorithm):
    """Ranked choice consensus - eliminates least preferred proposals."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via ranked choice.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal with highest confidence
        """
        if not proposals:
            return None

        # Simplified: use confidence scores as rankings
        ranked = sorted(proposals, key=lambda p: p.confidence, reverse=True)

        if ranked:
            return ranked[0]

        return None


class QuorumConsensus(ConsensusAlgorithm):
    """Quorum consensus - requires minimum participation and support threshold."""

    def __init__(self, quorum_threshold: float = 0.5):
        """Initialize with quorum threshold.

        Args:
            quorum_threshold: Minimum participation level (fraction of proposals)
        """
        self.quorum_threshold = quorum_threshold

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus with quorum requirement.

        Args:
            proposals: List of proposals

        Returns:
            Proposal if quorum is met and confidence is above threshold, or None
        """
        if not proposals:
            return None

        # Find proposal with highest confidence
        best_proposal = max(proposals, key=lambda p: p.confidence)

        # Check if we have quorum (minimum number of proposals submitted)
        min_participation = max(1, int(len(proposals) * self.quorum_threshold))
        if len(proposals) >= min_participation and best_proposal.confidence > 0.0:
            return best_proposal

        return None
