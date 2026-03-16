"""Consensus algorithms for reaching agreements between agents."""

from typing import Dict, Optional, Tuple

from socratic_conflict.core.conflict import Conflict


class ConsensusAlgorithm:
    """Base class for consensus algorithms."""

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus on a conflict.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, consensus_confidence) or None
        """
        raise NotImplementedError


class MajorityConsensus(ConsensusAlgorithm):
    """Majority consensus - proposal chosen by majority wins."""

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus via majority vote.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, confidence)
        """
        if not conflict.proposals:
            return None

        # Count agents supporting each proposal
        support_counts: Dict[str, int] = {}
        total_agents = len(conflict.related_agents)

        for proposal in conflict.proposals:
            support_counts[proposal.proposal_id] = support_counts.get(proposal.proposal_id, 0) + 1

        # Check for majority
        for proposal_id, count in support_counts.items():
            if count > total_agents / 2:
                confidence = count / total_agents
                return (proposal_id, confidence)

        return None


class UnanimousConsensus(ConsensusAlgorithm):
    """Unanimous consensus - all agents must agree."""

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus via unanimity.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, confidence) or None
        """
        if not conflict.proposals:
            return None

        total_agents = len(conflict.related_agents)

        for proposal in conflict.proposals:
            if len(conflict.related_agents) == total_agents:
                # Check if all agents support this
                supporting = sum(
                    1 for p in conflict.proposals if p.proposal_id == proposal.proposal_id
                )
                if supporting == total_agents:
                    return (proposal.proposal_id, 1.0)

        return None


class SupermajorityConsensus(ConsensusAlgorithm):
    """Supermajority consensus - 2/3 or 3/4 majority required."""

    def __init__(self, threshold: float = 2.0 / 3.0):
        """Initialize with threshold.

        Args:
            threshold: Required fraction (e.g., 0.67 for 2/3)
        """
        self.threshold = threshold

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus via supermajority.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, confidence)
        """
        if not conflict.proposals:
            return None

        support_counts: Dict[str, int] = {}
        total_agents = len(conflict.related_agents)

        for proposal in conflict.proposals:
            support_counts[proposal.proposal_id] = support_counts.get(proposal.proposal_id, 0) + 1

        for proposal_id, count in support_counts.items():
            if count / total_agents >= self.threshold:
                confidence = count / total_agents
                return (proposal_id, confidence)

        return None


class RankedChoiceConsensus(ConsensusAlgorithm):
    """Ranked choice consensus - eliminates least preferred proposals."""

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus via ranked choice.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, confidence)
        """
        if not conflict.proposals:
            return None

        # Simplified: use confidence scores as rankings
        ranked = sorted(conflict.proposals, key=lambda p: p.confidence, reverse=True)

        if ranked:
            confidence = ranked[0].confidence
            return (ranked[0].proposal_id, confidence)

        return None


class QuorumConsensus(ConsensusAlgorithm):
    """Quorum consensus - requires minimum participation threshold."""

    def __init__(self, quorum: float = 0.5):
        """Initialize with quorum threshold.

        Args:
            quorum: Minimum fraction of agents that must participate
        """
        self.quorum = quorum

    def reach_consensus(self, conflict: Conflict) -> Optional[Tuple[str, float]]:
        """Reach consensus with quorum requirement.

        Args:
            conflict: Conflict to resolve

        Returns:
            Tuple of (chosen_proposal_id, confidence)
        """
        if not conflict.proposals:
            return None

        total_agents = len(conflict.related_agents)
        participating = len(set(p.source_agent for p in conflict.proposals))

        # Check if quorum is met
        if participating / total_agents < self.quorum:
            return None

        # Use majority among those who participated
        support_counts: Dict[str, int] = {}
        for proposal in conflict.proposals:
            support_counts[proposal.proposal_id] = support_counts.get(proposal.proposal_id, 0) + 1

        if support_counts:
            proposal_id = max(support_counts, key=lambda pid: support_counts[pid])
            confidence = support_counts[proposal_id] / participating
            return (proposal_id, confidence)

        return None
