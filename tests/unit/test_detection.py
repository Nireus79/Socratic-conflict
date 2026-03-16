"""Unit tests for conflict detection."""

from socratic_conflict.detection.detector import ConflictDetector


class TestConflictDetector:
    """Test ConflictDetector."""

    def test_detector_creation(self):
        """Test creating a detector."""
        detector = ConflictDetector()
        assert detector.detected_conflicts == []

    def test_detect_data_conflict(self):
        """Test detecting data conflicts."""
        detector = ConflictDetector()

        values = {"agent1": "value_A", "agent2": "value_B"}
        conflict = detector.detect_data_conflict(
            field_name="temperature",
            values=values,
            agents=["agent1", "agent2"],
        )

        assert conflict is not None
        assert conflict.conflict_type == "data"
        assert len(conflict.proposals) == 2

    def test_no_data_conflict_identical_values(self):
        """Test that no conflict is detected for identical values."""
        detector = ConflictDetector()

        values = {"agent1": "value", "agent2": "value"}
        conflict = detector.detect_data_conflict(
            field_name="field",
            values=values,
            agents=["agent1", "agent2"],
        )

        assert conflict is None

    def test_detect_decision_conflict(self):
        """Test detecting decision conflicts."""
        detector = ConflictDetector()

        proposals = {
            "agent1": "Choose path A",
            "agent2": "Choose path B",
        }

        conflict = detector.detect_decision_conflict(
            decision_name="routing_decision",
            proposals=proposals,
            agents=["agent1", "agent2"],
        )

        assert conflict is not None
        assert conflict.conflict_type == "decision"
        assert len(conflict.proposals) == 2

    def test_no_decision_conflict_single_agent(self):
        """Test that no conflict is detected with single agent."""
        detector = ConflictDetector()

        proposals = {"agent1": "Proposal A"}

        conflict = detector.detect_decision_conflict(
            decision_name="decision",
            proposals=proposals,
            agents=["agent1"],
        )

        assert conflict is None

    def test_detect_workflow_conflict(self):
        """Test detecting workflow conflicts."""
        detector = ConflictDetector()

        steps = [
            {"step_id": "s1", "agent": "agent1", "action": "action_A"},
            {"step_id": "s2", "agent": "agent2", "action": "action_B"},
        ]

        conflict = detector.detect_workflow_conflict(
            workflow_id="wf1",
            conflicting_steps=steps,
        )

        assert conflict is not None
        assert conflict.conflict_type == "workflow"

    def test_get_conflicts(self):
        """Test retrieving conflicts."""
        detector = ConflictDetector()

        # Add a data conflict
        detector.detect_data_conflict(
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        # Add a decision conflict
        detector.detect_decision_conflict(
            decision_name="d1",
            proposals={"a": "p1", "b": "p2"},
            agents=["a", "b"],
        )

        all_conflicts = detector.get_conflicts()
        assert len(all_conflicts) == 2

        data_conflicts = detector.get_conflicts(conflict_type="data")
        assert len(data_conflicts) == 1

    def test_get_specific_conflict(self):
        """Test retrieving a specific conflict."""
        detector = ConflictDetector()

        conflict = detector.detect_data_conflict(
            field_name="field",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        found = detector.get_conflict(conflict.conflict_id)
        assert found is not None
        assert found.conflict_id == conflict.conflict_id

    def test_get_nonexistent_conflict(self):
        """Test retrieving nonexistent conflict."""
        detector = ConflictDetector()
        found = detector.get_conflict("nonexistent")
        assert found is None

    def test_clear_conflicts(self):
        """Test clearing conflicts."""
        detector = ConflictDetector()

        detector.detect_data_conflict(
            field_name="f",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        assert len(detector.detected_conflicts) == 1

        detector.clear_conflicts()
        assert len(detector.detected_conflicts) == 0

    def test_conflict_with_context(self):
        """Test conflict detection with context."""
        detector = ConflictDetector()

        context = {"workflow_id": "w1", "step": 3}
        conflict = detector.detect_data_conflict(
            field_name="field",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
            context=context,
        )

        assert conflict.context == context

    def test_severity_calculation(self):
        """Test severity calculation."""
        detector = ConflictDetector()

        # Two agents (not assigned, just triggering detection)
        detector.detect_data_conflict(
            field_name="f",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        # Three agents
        conflict3 = detector.detect_data_conflict(
            field_name="f",
            values={"a": "x", "b": "y", "c": "z"},
            agents=["a", "b", "c"],
        )

        # Higher severity for more agents
        assert conflict3.severity == "high"
