"""Resolution strategies for conflicts."""

from typing import Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, Proposal, Resolution


class ResolutionStrategy:
    """Base class for resolution strategies."""

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve a conflict using this strategy.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution object or None if unable to resolve
        """
        raise NotImplementedError


class VotingStrategy(ResolutionStrategy):
    """Simple voting strategy - choose proposal with most votes."""

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve conflict using voting.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution with voting results
        """
        if not conflict.proposals:
            return None

        # Simple voting - each agent votes for one proposal
        # Default: each agent votes for their own proposal
        votes: Dict[str, str] = {}
        for proposal in conflict.proposals:
            votes[proposal.source_agent] = proposal.proposal_id

        # Count votes
        vote_counts: Dict[str, int] = {}
        for proposal_id in votes.values():
            vote_counts[proposal_id] = vote_counts.get(proposal_id, 0) + 1

        # Find winner
        winner_id: Optional[str] = (
            max(vote_counts, key=lambda pid: vote_counts[pid]) if vote_counts else None
        )
        confidence = vote_counts[winner_id] / len(votes) if winner_id and votes else 0.0

        return Resolution(
            conflict_id=conflict.conflict_id,
            strategy="voting",
            recommended_proposal_id=winner_id,
            confidence=confidence,
            rationale=f"Voting strategy: {vote_counts}",
            votes=votes,
        )


class ConsensusStrategy(ResolutionStrategy):
    """Consensus strategy - find common ground or most acceptable proposal."""

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve conflict using consensus building.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution based on consensus
        """
        if not conflict.proposals:
            return None

        # Find proposal with highest average confidence
        best_proposal: Optional[Proposal] = None
        best_score = -1.0

        for proposal in conflict.proposals:
            score = proposal.confidence
            if score > best_score:
                best_score = score
                best_proposal = proposal

        if not best_proposal:
            return None

        return Resolution(
            conflict_id=conflict.conflict_id,
            strategy="consensus",
            recommended_proposal_id=best_proposal.proposal_id,
            confidence=best_score,
            rationale=f"Consensus: selected proposal with highest confidence ({best_score:.2f})",
        )


class WeightedStrategy(ResolutionStrategy):
    """Weighted strategy - combine proposals based on agent weights/expertise."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """Initialize with agent weights.

        Args:
            weights: Dict mapping agent names to weights (0.0-1.0)
        """
        self.weights = weights or {}

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve conflict using weighted scoring.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution based on weighted scores
        """
        if not conflict.proposals:
            return None

        # Score each proposal based on source agent weight and confidence
        proposal_scores: Dict[str, float] = {}

        for proposal in conflict.proposals:
            agent_weight = self.weights.get(proposal.source_agent, 0.5)
            score = agent_weight * proposal.confidence
            proposal_scores[proposal.proposal_id] = score

        # Find highest scored proposal
        best_proposal_id = max(proposal_scores, key=lambda pid: proposal_scores[pid])
        best_score = proposal_scores[best_proposal_id]

        return Resolution(
            conflict_id=conflict.conflict_id,
            strategy="weighted",
            recommended_proposal_id=best_proposal_id,
            confidence=best_score,
            rationale=f"Weighted scoring: {proposal_scores}",
        )


class PriorityStrategy(ResolutionStrategy):
    """Priority-based strategy - use predefined priority rules."""

    def __init__(self, priority_rules: Optional[Dict[str, int]] = None):
        """Initialize with priority rules.

        Args:
            priority_rules: Dict mapping agent names to priority levels
        """
        self.priority_rules = priority_rules or {}

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve conflict using priority rules.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution based on priorities
        """
        if not conflict.proposals:
            return None

        # Find proposal from highest priority agent
        best_proposal: Optional[Proposal] = None
        best_priority = -1

        for proposal in conflict.proposals:
            priority = self.priority_rules.get(proposal.source_agent, 0)
            if priority > best_priority:
                best_priority = priority
                best_proposal = proposal

        if not best_proposal:
            return None

        return Resolution(
            conflict_id=conflict.conflict_id,
            strategy="priority",
            recommended_proposal_id=best_proposal.proposal_id,
            confidence=0.8,  # High confidence for priority-based
            rationale=f"Priority-based: agent {best_proposal.source_agent} has priority level {best_priority}",
        )


class HybridStrategy(ResolutionStrategy):
    """Hybrid strategy - combine multiple strategies."""

    def __init__(self, strategies: Optional[List[ResolutionStrategy]] = None):
        """Initialize with multiple strategies.

        Args:
            strategies: List of strategies to combine
        """
        self.strategies = strategies or [VotingStrategy(), ConsensusStrategy()]

    def resolve(self, conflict: Conflict) -> Optional[Resolution]:
        """Resolve conflict using multiple strategies.

        Args:
            conflict: Conflict to resolve

        Returns:
            Resolution combining multiple strategies
        """
        resolutions = []
        for strategy in self.strategies:
            resolution = strategy.resolve(conflict)
            if resolution:
                resolutions.append(resolution)

        if not resolutions:
            return None

        # Combine resolutions - use the one with highest confidence
        best_resolution = max(resolutions, key=lambda r: r.confidence)
        best_resolution.strategy = "hybrid"
        best_resolution.rationale = f"Hybrid: combined {len(resolutions)} strategies"

        return best_resolution
