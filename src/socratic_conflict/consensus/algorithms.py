"""Consensus algorithms for reaching agreements between agents."""

from typing import TYPE_CHECKING, Dict, List, Optional

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
    """Majority consensus - proposal chosen by majority wins."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via majority vote.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal or None
        """
        if not proposals:
            return None

        # Count how many times each proposal appears (as a simple majority metric)
        support_counts: Dict[str, 'Proposal'] = {}
        count_map: Dict[str, int] = {}

        for proposal in proposals:
            pid = proposal.proposal_id
            if pid not in support_counts:
                support_counts[pid] = proposal
            count_map[pid] = count_map.get(pid, 0) + 1

        # Check for majority
        total = len(proposals)
        for pid, count in count_map.items():
            if count > total / 2:
                return support_counts[pid]

        return None


class UnanimousConsensus(ConsensusAlgorithm):
    """Unanimous consensus - all agents must agree."""

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via unanimity.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal or None if not unanimous
        """
        if not proposals:
            return None

        # Group by proposal_id and check if all proposals support the same option
        support_counts: Dict[str, int] = {}
        proposal_map: Dict[str, 'Proposal'] = {}

        for proposal in proposals:
            pid = proposal.proposal_id
            support_counts[pid] = support_counts.get(pid, 0) + 1
            if pid not in proposal_map:
                proposal_map[pid] = proposal

        # Check if any proposal has unanimous support
        total = len(proposals)
        for pid, count in support_counts.items():
            if count == total:
                return proposal_map[pid]

        return None


class SupermajorityConsensus(ConsensusAlgorithm):
    """Supermajority consensus - 2/3 or 3/4 majority required."""

    def __init__(self, threshold: float = 2.0 / 3.0):
        """Initialize with threshold.

        Args:
            threshold: Required fraction (e.g., 0.67 for 2/3)
        """
        self.threshold = threshold

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus via supermajority.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal or None
        """
        if not proposals:
            return None

        support_counts: Dict[str, int] = {}
        proposal_map: Dict[str, 'Proposal'] = {}

        for proposal in proposals:
            pid = proposal.proposal_id
            support_counts[pid] = support_counts.get(pid, 0) + 1
            if pid not in proposal_map:
                proposal_map[pid] = proposal

        total = len(proposals)
        for pid, count in support_counts.items():
            if count / total >= self.threshold:
                return proposal_map[pid]

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
    """Quorum consensus - requires minimum participation threshold."""

    def __init__(self, quorum_threshold: float = 0.5):
        """Initialize with quorum threshold.

        Args:
            quorum_threshold: Minimum fraction of agents that must participate
        """
        self.quorum_threshold = quorum_threshold

    def reach_consensus(self, proposals: List['Proposal']) -> Optional['Proposal']:
        """Reach consensus with quorum requirement.

        Args:
            proposals: List of proposals

        Returns:
            Chosen proposal or None if quorum not met
        """
        if not proposals:
            return None

        # Check participation threshold (use proposal count as proxy for participation)
        min_participation = max(1, int(len(proposals) * self.quorum_threshold))
        if len(proposals) < min_participation:
            return None

        # Use majority among those who participated
        support_counts: Dict[str, int] = {}
        proposal_map: Dict[str, 'Proposal'] = {}

        for proposal in proposals:
            pid = proposal.proposal_id
            support_counts[pid] = support_counts.get(pid, 0) + 1
            if pid not in proposal_map:
                proposal_map[pid] = proposal

        if support_counts:
            proposal_id = max(support_counts, key=lambda pid: support_counts[pid])
            return proposal_map[proposal_id]

        return None
