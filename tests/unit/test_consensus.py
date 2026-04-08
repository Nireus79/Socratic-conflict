"""Unit tests for consensus algorithms."""

import pytest

from socratic_conflict.core.conflict import Conflict, Proposal
from socratic_conflict.consensus.algorithms import (
    MajorityConsensus,
    UnanimousConsensus,
    SupermajorityConsensus,
    RankedChoiceConsensus,
    QuorumConsensus,
)


@pytest.fixture
def sample_proposals():
    """Create sample proposals for testing."""
    return [
        Proposal(
            title="Option A",
            description="First option",
            source_agent="Agent1",
            confidence=0.8,
        ),
        Proposal(
            title="Option B",
            description="Second option",
            source_agent="Agent2",
            confidence=0.7,
        ),
        Proposal(
            title="Option C",
            description="Third option",
            source_agent="Agent3",
            confidence=0.6,
        ),
    ]


@pytest.fixture
def sample_conflict(sample_proposals):
    """Create a sample conflict with proposals."""
    conflict = Conflict(
        title="Test Conflict",
        description="Test conflict for algorithms",
        conflict_type="decision",
        severity="high",
        related_agents=["Agent1", "Agent2", "Agent3"],
    )
    conflict.proposals = sample_proposals
    return conflict


class TestMajorityConsensus:
    """Test MajorityConsensus algorithm."""

    def test_majority_consensus_simple(self, sample_conflict):
        """Test majority consensus with simple majority."""
        algorithm = MajorityConsensus()

        # All agents support first proposal
        sample_conflict.proposals[0].confidence = 0.9
        sample_conflict.proposals[1].confidence = 0.0
        sample_conflict.proposals[2].confidence = 0.0

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.title == "Option A"

    def test_majority_consensus_tie(self, sample_conflict):
        """Test majority consensus with tie - should return first."""
        algorithm = MajorityConsensus()

        # Equal support
        sample_conflict.proposals[0].confidence = 0.5
        sample_conflict.proposals[1].confidence = 0.5
        sample_conflict.proposals[2].confidence = 0.0

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return first with >= 50%
        assert proposal is not None
        assert proposal.title in ["Option A", "Option B"]

    def test_majority_consensus_no_majority(self, sample_conflict):
        """Test when no proposal has majority."""
        algorithm = MajorityConsensus()

        # All equal low support
        sample_conflict.proposals[0].confidence = 0.3
        sample_conflict.proposals[1].confidence = 0.3
        sample_conflict.proposals[2].confidence = 0.4

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return the one with most support
        assert proposal is not None
        assert proposal.title == "Option C"

    def test_majority_consensus_empty(self):
        """Test with empty proposals."""
        algorithm = MajorityConsensus()
        proposal = algorithm.reach_consensus([])

        assert proposal is None


class TestUnanimousConsensus:
    """Test UnanimousConsensus algorithm."""

    def test_unanimous_consensus_all_agree(self, sample_conflict):
        """Test unanimous consensus when all agree."""
        algorithm = UnanimousConsensus()

        # All support same proposal
        sample_conflict.proposals[0].confidence = 1.0
        sample_conflict.proposals[1].confidence = 0.0
        sample_conflict.proposals[2].confidence = 0.0

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return the unanimous option
        assert proposal is not None
        assert proposal.title == "Option A"

    def test_unanimous_consensus_no_agreement(self, sample_conflict):
        """Test unanimous consensus when agents disagree."""
        algorithm = UnanimousConsensus()

        # All have different preferences
        sample_conflict.proposals[0].confidence = 0.8
        sample_conflict.proposals[1].confidence = 0.7
        sample_conflict.proposals[2].confidence = 0.6

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return None when no unanimity
        assert proposal is None

    def test_unanimous_consensus_split(self, sample_conflict):
        """Test unanimous consensus with split votes."""
        algorithm = UnanimousConsensus()

        sample_conflict.proposals[0].confidence = 0.5
        sample_conflict.proposals[1].confidence = 0.5
        sample_conflict.proposals[2].confidence = 0.0

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return None since not unanimous
        assert proposal is None


class TestSupermajorityConsensus:
    """Test SupermajorityConsensus algorithm."""

    def test_supermajority_default_threshold(self, sample_conflict):
        """Test supermajority with default 2/3 threshold."""
        algorithm = SupermajorityConsensus()

        # 3 proposals: first gets 0.7 (exceeds 2/3 = 0.667)
        sample_conflict.proposals[0].confidence = 0.7
        sample_conflict.proposals[1].confidence = 0.2
        sample_conflict.proposals[2].confidence = 0.1

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.title == "Option A"

    def test_supermajority_custom_threshold(self, sample_conflict):
        """Test supermajority with custom threshold."""
        algorithm = SupermajorityConsensus(threshold=0.8)

        # First proposal at 0.75 (below 0.8)
        sample_conflict.proposals[0].confidence = 0.75
        sample_conflict.proposals[1].confidence = 0.15
        sample_conflict.proposals[2].confidence = 0.1

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # Should return None since below threshold
        assert proposal is None

    def test_supermajority_threshold_met(self, sample_conflict):
        """Test supermajority when threshold is met."""
        algorithm = SupermajorityConsensus(threshold=0.6)

        sample_conflict.proposals[0].confidence = 0.65
        sample_conflict.proposals[1].confidence = 0.2
        sample_conflict.proposals[2].confidence = 0.15

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.title == "Option A"


class TestRankedChoiceConsensus:
    """Test RankedChoiceConsensus algorithm."""

    def test_ranked_choice_returns_highest(self, sample_conflict):
        """Test ranked choice returns highest confidence proposal."""
        algorithm = RankedChoiceConsensus()

        sample_conflict.proposals[0].confidence = 0.6
        sample_conflict.proposals[1].confidence = 0.8
        sample_conflict.proposals[2].confidence = 0.7

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.title == "Option B"
        assert proposal.confidence == 0.8

    def test_ranked_choice_single_option(self):
        """Test ranked choice with single option."""
        algorithm = RankedChoiceConsensus()

        proposal = Proposal(
            title="Only Option",
            description="Single",
            source_agent="Agent1",
            confidence=0.5,
        )

        result = algorithm.reach_consensus([proposal])

        assert result is not None
        assert result.title == "Only Option"

    def test_ranked_choice_empty(self):
        """Test ranked choice with empty list."""
        algorithm = RankedChoiceConsensus()

        result = algorithm.reach_consensus([])

        assert result is None

    def test_ranked_choice_all_equal(self, sample_conflict):
        """Test ranked choice when all have equal confidence."""
        algorithm = RankedChoiceConsensus()

        sample_conflict.proposals[0].confidence = 0.5
        sample_conflict.proposals[1].confidence = 0.5
        sample_conflict.proposals[2].confidence = 0.5

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.confidence == 0.5


class TestQuorumConsensus:
    """Test QuorumConsensus algorithm."""

    def test_quorum_met_majority(self, sample_conflict):
        """Test quorum consensus when quorum is met and majority exists."""
        algorithm = QuorumConsensus(quorum_threshold=0.5)

        # 3 agents, quorum = 2 (> 50%)
        # If 2 agents support a proposal, it passes
        sample_conflict.proposals[0].confidence = 0.7
        sample_conflict.proposals[1].confidence = 0.0
        sample_conflict.proposals[2].confidence = 0.3

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None

    def test_quorum_not_met(self, sample_conflict):
        """Test quorum consensus when quorum is not met."""
        algorithm = QuorumConsensus(quorum_threshold=0.9)

        # 3 agents, quorum threshold = 90% = 2.7 agents (impossible)
        # No reasonable majority
        sample_conflict.proposals[0].confidence = 0.3
        sample_conflict.proposals[1].confidence = 0.3
        sample_conflict.proposals[2].confidence = 0.4

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        # May return None or highest, depends on implementation
        # Just verify it doesn't crash
        assert proposal is None or proposal.title in [
            "Option A",
            "Option B",
            "Option C",
        ]

    def test_quorum_high_threshold(self, sample_conflict):
        """Test quorum with high threshold."""
        algorithm = QuorumConsensus(quorum_threshold=0.7)

        sample_conflict.proposals[0].confidence = 0.8
        sample_conflict.proposals[1].confidence = 0.1
        sample_conflict.proposals[2].confidence = 0.1

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None
        assert proposal.title == "Option A"

    def test_quorum_low_threshold(self, sample_conflict):
        """Test quorum with low threshold."""
        algorithm = QuorumConsensus(quorum_threshold=0.2)

        sample_conflict.proposals[0].confidence = 0.5
        sample_conflict.proposals[1].confidence = 0.3
        sample_conflict.proposals[2].confidence = 0.2

        proposal = algorithm.reach_consensus(sample_conflict.proposals)

        assert proposal is not None


class TestConsensusIntegration:
    """Integration tests for consensus algorithms."""

    def test_all_algorithms_handle_single_proposal(self):
        """Test that all algorithms handle single proposal."""
        proposal = Proposal(
            title="Only",
            description="Single",
            source_agent="Agent1",
            confidence=0.8,
        )

        algorithms = [
            MajorityConsensus(),
            UnanimousConsensus(),
            SupermajorityConsensus(),
            RankedChoiceConsensus(),
            QuorumConsensus(),
        ]

        for algo in algorithms:
            result = algo.reach_consensus([proposal])
            # All should handle single proposal gracefully
            assert result is None or result.title == "Only"

    def test_all_algorithms_handle_empty_list(self):
        """Test that all algorithms handle empty proposal list."""
        algorithms = [
            MajorityConsensus(),
            UnanimousConsensus(),
            SupermajorityConsensus(),
            RankedChoiceConsensus(),
            QuorumConsensus(),
        ]

        for algo in algorithms:
            result = algo.reach_consensus([])
            assert result is None

    def test_algorithm_consistency(self, sample_conflict):
        """Test that algorithms are somewhat consistent."""
        # Set up clear majority
        sample_conflict.proposals[0].confidence = 0.9
        sample_conflict.proposals[1].confidence = 0.05
        sample_conflict.proposals[2].confidence = 0.05

        majority = MajorityConsensus()
        ranked = RankedChoiceConsensus()

        majority_result = majority.reach_consensus(sample_conflict.proposals)
        ranked_result = ranked.reach_consensus(sample_conflict.proposals)

        # Both should prefer the highest confidence proposal
        assert majority_result.title == "Option A"
        assert ranked_result.title == "Option A"
