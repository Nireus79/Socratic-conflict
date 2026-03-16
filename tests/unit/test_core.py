"""Unit tests for core conflict models."""

from socratic_conflict.core.conflict import Conflict, ConflictDecision, Proposal, Resolution


class TestProposal:
    """Test Proposal model."""

    def test_proposal_creation(self):
        """Test creating a proposal."""
        proposal = Proposal(
            title="Proposal A",
            description="This is proposal A",
            source_agent="agent1",
            confidence=0.8,
        )
        assert proposal.title == "Proposal A"
        assert proposal.source_agent == "agent1"
        assert proposal.confidence == 0.8
        assert proposal.proposal_id is not None

    def test_proposal_serialization(self):
        """Test proposal to/from dict."""
        proposal = Proposal(
            title="Test",
            source_agent="agent1",
            confidence=0.75,
        )
        data = proposal.to_dict()
        assert data["title"] == "Test"
        assert data["source_agent"] == "agent1"

        restored = Proposal.from_dict(data)
        assert restored.title == proposal.title
        assert restored.source_agent == proposal.source_agent
        assert restored.confidence == proposal.confidence

    def test_proposal_default_values(self):
        """Test proposal default values."""
        proposal = Proposal()
        assert proposal.title == ""
        assert proposal.confidence == 0.0
        assert proposal.proposed_at is not None


class TestConflict:
    """Test Conflict model."""

    def test_conflict_creation(self):
        """Test creating a conflict."""
        conflict = Conflict(
            title="Data Conflict",
            conflict_type="data",
            related_agents=["agent1", "agent2"],
        )
        assert conflict.title == "Data Conflict"
        assert conflict.conflict_type == "data"
        assert len(conflict.related_agents) == 2
        assert conflict.conflict_id is not None

    def test_conflict_with_proposals(self):
        """Test conflict with proposals."""
        proposal1 = Proposal(title="Option A", source_agent="agent1")
        proposal2 = Proposal(title="Option B", source_agent="agent2")

        conflict = Conflict(
            title="Test Conflict",
            proposals=[proposal1, proposal2],
        )

        assert len(conflict.proposals) == 2
        assert conflict.proposals[0].title == "Option A"

    def test_conflict_serialization(self):
        """Test conflict to/from dict."""
        proposal = Proposal(title="Test", source_agent="agent1")
        conflict = Conflict(
            title="Conflict",
            conflict_type="decision",
            proposals=[proposal],
        )

        data = conflict.to_dict()
        assert data["title"] == "Conflict"
        assert len(data["proposals"]) == 1

        restored = Conflict.from_dict(data)
        assert restored.title == conflict.title
        assert len(restored.proposals) == 1

    def test_conflict_severity_levels(self):
        """Test conflict severity levels."""
        for severity in ["low", "medium", "high", "critical"]:
            conflict = Conflict(severity=severity)
            assert conflict.severity == severity


class TestResolution:
    """Test Resolution model."""

    def test_resolution_creation(self):
        """Test creating a resolution."""
        resolution = Resolution(
            conflict_id="conflict1",
            strategy="voting",
            recommended_proposal_id="proposal1",
            confidence=0.9,
        )
        assert resolution.conflict_id == "conflict1"
        assert resolution.strategy == "voting"
        assert resolution.confidence == 0.9

    def test_resolution_with_votes(self):
        """Test resolution with voting data."""
        resolution = Resolution(
            conflict_id="conflict1",
            strategy="voting",
            votes={"agent1": "p1", "agent2": "p1", "agent3": "p2"},
        )
        assert len(resolution.votes) == 3
        assert resolution.votes["agent1"] == "p1"

    def test_resolution_serialization(self):
        """Test resolution to/from dict."""
        resolution = Resolution(
            conflict_id="c1",
            strategy="consensus",
            confidence=0.75,
        )

        data = resolution.to_dict()
        assert data["conflict_id"] == "c1"
        assert data["strategy"] == "consensus"

        restored = Resolution.from_dict(data)
        assert restored.conflict_id == resolution.conflict_id
        assert restored.strategy == resolution.strategy


class TestConflictDecision:
    """Test ConflictDecision model."""

    def test_decision_creation(self):
        """Test creating a decision."""
        decision = ConflictDecision(
            conflict_id="c1",
            chosen_proposal_id="p1",
            decided_by="admin",
        )
        assert decision.conflict_id == "c1"
        assert decision.chosen_proposal_id == "p1"
        assert decision.decided_by == "admin"
        assert decision.version == 1

    def test_decision_versioning(self):
        """Test decision versioning."""
        d1 = ConflictDecision(
            conflict_id="c1",
            chosen_proposal_id="p1",
            version=1,
        )
        d2 = ConflictDecision(
            conflict_id="c1",
            chosen_proposal_id="p2",
            version=2,
        )
        assert d2.version > d1.version

    def test_decision_serialization(self):
        """Test decision to/from dict."""
        decision = ConflictDecision(
            conflict_id="c1",
            chosen_proposal_id="p1",
            decided_by="system",
        )

        data = decision.to_dict()
        assert data["conflict_id"] == "c1"

        restored = ConflictDecision.from_dict(data)
        assert restored.conflict_id == decision.conflict_id
        assert restored.chosen_proposal_id == decision.chosen_proposal_id
