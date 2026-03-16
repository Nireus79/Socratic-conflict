"""Unit tests for resolution strategies."""

from socratic_conflict.core.conflict import Conflict, Proposal
from socratic_conflict.resolution.strategies import (
    ConsensusStrategy,
    HybridStrategy,
    PriorityStrategy,
    VotingStrategy,
    WeightedStrategy,
)


class TestVotingStrategy:
    """Test VotingStrategy."""

    def test_voting_resolution(self):
        """Test voting strategy."""
        proposal1 = Proposal(
            title="Option A",
            source_agent="agent1",
            confidence=0.7,
        )
        proposal2 = Proposal(
            title="Option B",
            source_agent="agent2",
            confidence=0.8,
        )

        conflict = Conflict(
            title="Test",
            proposals=[proposal1, proposal2],
            related_agents=["agent1", "agent2"],
        )

        strategy = VotingStrategy()
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        assert resolution.strategy == "voting"
        assert resolution.recommended_proposal_id is not None

    def test_voting_with_three_proposals(self):
        """Test voting with three proposals."""
        proposals = [
            Proposal(title=f"Option {i}", source_agent=f"agent{i}", confidence=0.5)
            for i in range(3)
        ]

        conflict = Conflict(
            proposals=proposals,
            related_agents=[f"agent{i}" for i in range(3)],
        )

        strategy = VotingStrategy()
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        assert resolution.confidence > 0


class TestConsensusStrategy:
    """Test ConsensusStrategy."""

    def test_consensus_resolution(self):
        """Test consensus strategy."""
        proposal1 = Proposal(
            title="Option A",
            source_agent="agent1",
            confidence=0.5,
        )
        proposal2 = Proposal(
            title="Option B",
            source_agent="agent2",
            confidence=0.9,  # Highest confidence
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategy = ConsensusStrategy()
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        assert resolution.recommended_proposal_id == proposal2.proposal_id
        assert resolution.confidence == 0.9


class TestWeightedStrategy:
    """Test WeightedStrategy."""

    def test_weighted_resolution(self):
        """Test weighted strategy."""
        weights = {"expert_agent": 0.9, "junior_agent": 0.3}

        proposal1 = Proposal(
            title="Expert Opinion",
            source_agent="expert_agent",
            confidence=0.7,
        )
        proposal2 = Proposal(
            title="Junior Opinion",
            source_agent="junior_agent",
            confidence=0.9,
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategy = WeightedStrategy(weights=weights)
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        # Expert opinion should win despite lower confidence
        assert resolution.recommended_proposal_id == proposal1.proposal_id

    def test_weighted_without_weights(self):
        """Test weighted strategy without predefined weights."""
        proposal1 = Proposal(
            title="Option A",
            source_agent="agent1",
            confidence=0.8,
        )
        proposal2 = Proposal(
            title="Option B",
            source_agent="agent2",
            confidence=0.6,
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategy = WeightedStrategy()  # Default weights
        resolution = strategy.resolve(conflict)

        assert resolution is not None


class TestPriorityStrategy:
    """Test PriorityStrategy."""

    def test_priority_resolution(self):
        """Test priority strategy."""
        priorities = {"high_priority_agent": 10, "low_priority_agent": 1}

        proposal1 = Proposal(
            title="Low Priority Opinion",
            source_agent="low_priority_agent",
            confidence=0.95,
        )
        proposal2 = Proposal(
            title="High Priority Opinion",
            source_agent="high_priority_agent",
            confidence=0.5,
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategy = PriorityStrategy(priority_rules=priorities)
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        # High priority should win
        assert resolution.recommended_proposal_id == proposal2.proposal_id


class TestHybridStrategy:
    """Test HybridStrategy."""

    def test_hybrid_resolution(self):
        """Test hybrid strategy combining multiple strategies."""
        proposal1 = Proposal(
            title="Option A",
            source_agent="agent1",
            confidence=0.7,
        )
        proposal2 = Proposal(
            title="Option B",
            source_agent="agent2",
            confidence=0.8,
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategy = HybridStrategy()
        resolution = strategy.resolve(conflict)

        assert resolution is not None
        assert resolution.strategy == "hybrid"

    def test_hybrid_custom_strategies(self):
        """Test hybrid with custom strategies."""
        proposal1 = Proposal(
            title="Option A",
            source_agent="agent1",
            confidence=0.7,
        )
        proposal2 = Proposal(
            title="Option B",
            source_agent="agent2",
            confidence=0.8,
        )

        conflict = Conflict(proposals=[proposal1, proposal2])

        strategies = [ConsensusStrategy(), VotingStrategy()]
        hybrid = HybridStrategy(strategies=strategies)
        resolution = hybrid.resolve(conflict)

        assert resolution is not None
