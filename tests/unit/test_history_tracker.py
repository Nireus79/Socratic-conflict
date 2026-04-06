"""Unit tests for HistoryTracker."""

import pytest

from socratic_conflict.history.tracker import HistoryTracker
from socratic_conflict.core.conflict import Conflict, Proposal, Resolution, ConflictDecision


@pytest.fixture
def tracker():
    """Create a HistoryTracker instance."""
    return HistoryTracker()


@pytest.fixture
def sample_conflict():
    """Create a sample conflict."""
    conflict = Conflict(
        title="Test Conflict",
        description="Testing conflict tracking",
        conflict_type="data",
        severity="high",
        related_agents=["Agent1", "Agent2"],
    )
    conflict.proposals = [
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
    ]
    return conflict


@pytest.fixture
def sample_resolution(sample_conflict):
    """Create a sample resolution."""
    return Resolution(
        conflict_id=sample_conflict.conflict_id,
        strategy="voting",
        recommended_proposal_id=sample_conflict.proposals[0].proposal_id,
        confidence=0.85,
    )


@pytest.fixture
def sample_decision(sample_conflict):
    """Create a sample conflict decision."""
    return ConflictDecision(
        conflict_id=sample_conflict.conflict_id,
        chosen_proposal_id=sample_conflict.proposals[0].proposal_id,
        decided_by="Arbitrator",
    )


class TestHistoryTrackerBasic:
    """Test basic HistoryTracker functionality."""

    def test_tracker_initialization(self, tracker):
        """Test tracker initializes with empty history."""
        assert tracker.conflict_history == {}
        assert tracker.resolution_history == {}
        assert tracker.decision_history == {}

    def test_add_conflict(self, tracker, sample_conflict):
        """Test adding a conflict to history."""
        tracker.add_conflict(sample_conflict)

        assert sample_conflict.conflict_id in tracker.conflict_history
        assert tracker.conflict_history[sample_conflict.conflict_id] == sample_conflict

    def test_add_multiple_conflicts(self, tracker):
        """Test adding multiple conflicts."""
        conflicts = []
        for i in range(5):
            conflict = Conflict(
                title=f"Conflict {i}",
                description=f"Testing conflict {i}",
                conflict_type="data",
                severity="medium",
                related_agents=[f"Agent{i}"],
            )
            conflicts.append(conflict)
            tracker.add_conflict(conflict)

        assert len(tracker.conflict_history) == 5
        for conflict in conflicts:
            assert conflict.conflict_id in tracker.conflict_history

    def test_add_resolution(self, tracker, sample_resolution):
        """Test adding a resolution to history."""
        tracker.add_resolution(sample_resolution)

        assert sample_resolution.resolution_id in tracker.resolution_history
        assert tracker.resolution_history[sample_resolution.resolution_id] == sample_resolution

    def test_add_decision(self, tracker, sample_decision):
        """Test adding a decision to history."""
        tracker.add_decision(sample_decision)

        assert sample_decision.decided_at is not None
        assert sample_decision.conflict_id in tracker.decision_history


class TestHistoryTrackerRetrieval:
    """Test history retrieval methods."""

    def test_get_conflict_history_basic(self, tracker, sample_conflict):
        """Test retrieving conflict history."""
        tracker.add_conflict(sample_conflict)

        history = tracker.get_conflict_history(sample_conflict.conflict_id)

        assert len(history["conflicts"]) == 1
        assert history["conflicts"][0].conflict_id == sample_conflict.conflict_id

    def test_get_conflict_history_with_resolutions(
        self, tracker, sample_conflict, sample_resolution
    ):
        """Test conflict history includes associated resolutions."""
        tracker.add_conflict(sample_conflict)
        tracker.add_resolution(sample_resolution)

        history = tracker.get_conflict_history(sample_conflict.conflict_id)

        assert "conflicts" in history
        assert "resolutions" in history
        assert len(history["resolutions"]) == 1

    def test_get_conflict_history_nonexistent(self, tracker):
        """Test getting history for non-existent conflict."""
        history = tracker.get_conflict_history("nonexistent")

        assert len(history["conflicts"]) == 0

    def test_get_agent_conflict_history(self, tracker):
        """Test retrieving history for specific agent."""
        conflict1 = Conflict(
            title="Conflict 1",
            description="Agent A involved",
            conflict_type="data",
            severity="medium",
            related_agents=["AgentA", "AgentB"],
        )
        conflict2 = Conflict(
            title="Conflict 2",
            description="Different agents",
            conflict_type="data",
            severity="medium",
            related_agents=["AgentC", "AgentD"],
        )

        tracker.add_conflict(conflict1)
        tracker.add_conflict(conflict2)

        agent_a_history = tracker.get_agent_conflict_history("AgentA")

        assert len(agent_a_history) == 1
        assert agent_a_history[0].conflict_id == conflict1.conflict_id

    def test_get_agent_conflict_history_multiple(self, tracker):
        """Test agent with multiple conflicts."""
        conflicts = []
        for i in range(3):
            conflict = Conflict(
                title=f"Conflict {i}",
                description="AgentX involved",
                conflict_type="data",
                severity="medium",
                related_agents=["AgentX", f"Agent{i}"],
            )
            conflicts.append(conflict)
            tracker.add_conflict(conflict)

        history = tracker.get_agent_conflict_history("AgentX")

        assert len(history) == 3


class TestHistoryTrackerStatistics:
    """Test statistics generation."""

    def test_get_statistics_empty(self, tracker):
        """Test statistics with no history."""
        stats = tracker.get_statistics()

        assert stats["total_conflicts"] == 0
        assert stats["by_type"] == {}
        assert stats["by_severity"] == {}
        assert stats["resolved_count"] == 0

    def test_get_statistics_with_conflicts(self, tracker):
        """Test statistics with conflicts."""
        conflicts = []
        for i in range(5):
            conflict = Conflict(
                title=f"Conflict {i}",
                description="Testing",
                conflict_type="data" if i < 3 else "decision",
                severity="high" if i < 2 else "medium",
                related_agents=["Agent1"],
            )
            conflicts.append(conflict)
            tracker.add_conflict(conflict)

        stats = tracker.get_statistics()

        assert stats["total_conflicts"] == 5
        assert stats["by_type"]["data"] == 3
        assert stats["by_type"]["decision"] == 2
        assert stats["by_severity"]["high"] == 2
        assert stats["by_severity"]["medium"] == 3

    def test_get_statistics_with_resolutions(
        self, tracker, sample_conflict, sample_resolution
    ):
        """Test statistics include resolution count."""
        tracker.add_conflict(sample_conflict)
        tracker.add_resolution(sample_resolution)

        stats = tracker.get_statistics()

        assert stats["total_conflicts"] == 1
        assert stats["total_resolutions"] == 1

    def test_get_statistics_resolution_rate(self, tracker):
        """Test resolution rate calculation."""
        # Create 10 conflicts
        for i in range(10):
            conflict = Conflict(
                title=f"Conflict {i}",
                description="Testing",
                conflict_type="data",
                severity="medium",
                related_agents=["Agent1"],
            )
            tracker.add_conflict(conflict)

            # Resolve only first 7
            if i < 7:
                resolution = Resolution(
                    conflict_id=conflict.conflict_id,
                    strategy="voting",
                    recommended_proposal_id="prop_1",
                    confidence=0.8,
                )
                tracker.add_resolution(resolution)

        stats = tracker.get_statistics()

        assert stats["total_conflicts"] == 10
        assert stats["total_resolutions"] == 7
        assert stats["resolution_rate"] == 70.0


class TestHistoryTrackerVersioning:
    """Test decision versioning."""

    def test_get_decision_versions_empty(self, tracker):
        """Test getting versions for non-existent conflict."""
        versions = tracker.get_decision_versions("nonexistent")

        assert len(versions) == 0

    def test_get_decision_versions_single(
        self, tracker, sample_conflict, sample_decision
    ):
        """Test getting single decision version."""
        tracker.add_conflict(sample_conflict)
        tracker.add_decision(sample_decision)

        versions = tracker.get_decision_versions(sample_conflict.conflict_id)

        assert len(versions) == 1
        assert versions[0].conflict_id == sample_conflict.conflict_id

    def test_revert_decision_creates_version(
        self, tracker, sample_conflict, sample_decision
    ):
        """Test that reverting creates new version."""
        tracker.add_conflict(sample_conflict)
        tracker.add_decision(sample_decision)

        # Revert with new decision
        new_decision = ConflictDecision(
            conflict_id=sample_conflict.conflict_id,
            chosen_proposal_id=sample_conflict.conflict_id,
            decided_by="Arbitrator2",
        )

        tracker.revert_decision(sample_conflict.conflict_id, new_decision)

        versions = tracker.get_decision_versions(sample_conflict.conflict_id)

        assert len(versions) == 2
        assert versions[-1].decided_by == "Arbitrator2"
        assert versions[-1].version == 2

    def test_decision_version_numbering(self, tracker, sample_conflict):
        """Test decision version numbers increment."""
        tracker.add_conflict(sample_conflict)

        decisions = []
        for i in range(3):
            decision = ConflictDecision(
                conflict_id=sample_conflict.conflict_id,
                chosen_proposal_id="prop_id",
                decided_by=f"Decider{i}",
            )
            if i == 0:
                tracker.add_decision(decision)
            else:
                tracker.revert_decision(sample_conflict.conflict_id, decision)
            decisions.append(decision)

        versions = tracker.get_decision_versions(sample_conflict.conflict_id)

        assert len(versions) == 3
        assert versions[0].version == 1
        assert versions[1].version == 2
        assert versions[2].version == 3


class TestHistoryTrackerClear:
    """Test clearing history."""

    def test_clear_history(self, tracker, sample_conflict, sample_resolution):
        """Test clearing entire history."""
        tracker.add_conflict(sample_conflict)
        tracker.add_resolution(sample_resolution)

        assert len(tracker.conflict_history) > 0
        assert len(tracker.resolution_history) > 0

        tracker.clear_history()

        assert len(tracker.conflict_history) == 0
        assert len(tracker.resolution_history) == 0
        assert len(tracker.decision_history) == 0

    def test_clear_history_returns_stats(
        self, tracker, sample_conflict, sample_resolution
    ):
        """Test that clear_history returns statistics."""
        tracker.add_conflict(sample_conflict)
        tracker.add_resolution(sample_resolution)

        stats = tracker.clear_history()

        assert stats["cleared_conflicts"] == 1
        assert stats["cleared_resolutions"] == 1


class TestHistoryTrackerIntegration:
    """Integration tests for HistoryTracker."""

    def test_full_workflow(self, tracker):
        """Test full conflict resolution workflow with tracking."""
        # Create conflict
        conflict = Conflict(
            title="Integration Test Conflict",
            description="Testing full workflow",
            conflict_type="decision",
            severity="high",
            related_agents=["Agent1", "Agent2", "Agent3"],
        )
        conflict.proposals = [
            Proposal(
                title="Proposal A",
                description="First",
                source_agent="Agent1",
                confidence=0.8,
            ),
            Proposal(
                title="Proposal B",
                description="Second",
                source_agent="Agent2",
                confidence=0.7,
            ),
        ]

        # Add to history
        tracker.add_conflict(conflict)

        # Create resolution
        resolution = Resolution(
            conflict_id=conflict.conflict_id,
            strategy="voting",
            recommended_proposal_id=conflict.proposals[0].proposal_id,
            confidence=0.85,
        )
        tracker.add_resolution(resolution)

        # Create decision
        decision = ConflictDecision(
            conflict_id=conflict.conflict_id,
            chosen_proposal_id=conflict.proposals[0].proposal_id,
            decided_by="Arbitrator",
        )
        tracker.add_decision(decision)

        # Verify full history
        conflict_hist = tracker.get_conflict_history(conflict.conflict_id)
        assert len(conflict_hist["conflicts"]) == 1
        assert len(conflict_hist["resolutions"]) == 1
        assert len(conflict_hist["decisions"]) == 1

        # Get statistics
        stats = tracker.get_statistics()
        assert stats["total_conflicts"] == 1
        assert stats["total_resolutions"] == 1
        assert stats["resolved_count"] == 1
        assert stats["resolution_rate"] == 100.0

    def test_multiple_conflicts_tracking(self, tracker):
        """Test tracking multiple independent conflicts."""
        conflicts = []
        for i in range(3):
            conflict = Conflict(
                title=f"Conflict {i}",
                description=f"Test conflict {i}",
                conflict_type="data",
                severity="medium",
                related_agents=[f"Agent{i}"],
            )
            conflicts.append(conflict)
            tracker.add_conflict(conflict)

            # Add different number of resolutions
            for j in range(i + 1):
                resolution = Resolution(
                    conflict_id=conflict.conflict_id,
                    strategy="consensus",
                    recommended_proposal_id="prop_id",
                    confidence=0.8 - (j * 0.1),
                )
                tracker.add_resolution(resolution)

        stats = tracker.get_statistics()

        assert stats["total_conflicts"] == 3
        assert stats["total_resolutions"] == 6  # 1 + 2 + 3
