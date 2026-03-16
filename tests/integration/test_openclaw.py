"""Integration tests for Openclaw skill."""

from socratic_conflict.integrations.openclaw import SocraticConflictSkill


class TestSocraticConflictSkill:
    """Test SocraticConflictSkill Openclaw integration."""

    def test_skill_creation(self) -> None:
        """Test creating the skill."""
        skill = SocraticConflictSkill()
        assert skill is not None

    def test_data_conflict_detection(self) -> None:
        """Test detecting data conflicts."""
        skill = SocraticConflictSkill()

        result = skill.detect_data_conflict(
            field_name="priority",
            values={"agent1": "high", "agent2": "low"},
            agents=["agent1", "agent2"],
        )

        assert result is not None
        assert result["conflict_type"] == "data"
        assert result["severity"] == "medium"

    def test_decision_conflict_detection(self) -> None:
        """Test detecting decision conflicts."""
        skill = SocraticConflictSkill()

        result = skill.detect_decision_conflict(
            decision_name="routing",
            proposals={"agent1": "Path A", "agent2": "Path B"},
            agents=["agent1", "agent2"],
        )

        assert result is not None
        assert result["conflict_type"] == "decision"

    def test_workflow_conflict_detection(self) -> None:
        """Test detecting workflow conflicts."""
        skill = SocraticConflictSkill()

        result = skill.detect_workflow_conflict(
            workflow_id="pipeline",
            conflicting_steps=[
                {"step_id": "s1", "agent": "a1", "action": "process"},
                {"step_id": "s2", "agent": "a2", "action": "skip"},
            ],
        )

        assert result is not None
        assert result["conflict_type"] == "workflow"

    def test_voting_resolution(self) -> None:
        """Test voting strategy resolution."""
        skill = SocraticConflictSkill()

        # First detect
        conflict_result = skill.detect_data_conflict(
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = conflict_result["conflict_id"]

        # Then resolve with voting
        resolution = skill.resolve_with_strategy(conflict_id, strategy="voting")

        assert resolution is not None
        assert "recommended_proposal_id" in resolution

    def test_consensus_resolution(self) -> None:
        """Test consensus strategy resolution."""
        skill = SocraticConflictSkill()

        conflict_result = skill.detect_data_conflict(
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = conflict_result["conflict_id"]

        resolution = skill.resolve_with_strategy(conflict_id, strategy="consensus")

        assert resolution is not None
        assert resolution["strategy"] == "consensus"

    def test_weighted_resolution(self) -> None:
        """Test weighted strategy resolution."""
        skill = SocraticConflictSkill()

        conflict_result = skill.detect_data_conflict(
            field_name="value",
            values={"expert": "x", "junior": "y"},
            agents=["expert", "junior"],
        )
        conflict_id = conflict_result["conflict_id"]

        resolution = skill.resolve_with_strategy(
            conflict_id,
            strategy="weighted",
            strategy_config={"weights": {"expert": 0.8, "junior": 0.3}},
        )

        assert resolution is not None
        assert resolution["strategy"] == "weighted"

    def test_priority_resolution(self) -> None:
        """Test priority strategy resolution."""
        skill = SocraticConflictSkill()

        conflict_result = skill.detect_decision_conflict(
            decision_name="action",
            proposals={"user": "A", "admin": "B"},
            agents=["user", "admin"],
        )
        conflict_id = conflict_result["conflict_id"]

        resolution = skill.resolve_with_strategy(
            conflict_id,
            strategy="priority",
            strategy_config={"priority_rules": {"admin": 10, "user": 1}},
        )

        assert resolution is not None
        assert resolution["strategy"] == "priority"

    def test_make_decision(self) -> None:
        """Test making a final decision."""
        skill = SocraticConflictSkill()

        conflict_result = skill.detect_data_conflict(
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = conflict_result["conflict_id"]

        decision = skill.make_decision(
            conflict_id=conflict_id,
            chosen_proposal_id="p1",
            decided_by="admin",
            reason="Admin override",
        )

        assert decision is not None
        assert decision["conflict_id"] == conflict_id
        assert decision["chosen_proposal_id"] == "p1"

    def test_conflict_summary(self) -> None:
        """Test getting conflict summary."""
        skill = SocraticConflictSkill()

        conflict_result = skill.detect_data_conflict(
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = conflict_result["conflict_id"]

        summary = skill.get_conflict_summary(conflict_id)

        assert summary is not None
        assert summary["status"] == "unresolved"

    def test_list_conflicts(self) -> None:
        """Test listing conflicts."""
        skill = SocraticConflictSkill()

        # Add multiple conflicts
        skill.detect_data_conflict(
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        skill.detect_decision_conflict(
            decision_name="d1",
            proposals={"a": "p1", "b": "p2"},
            agents=["a", "b"],
        )

        conflicts = skill.list_conflicts()
        assert len(conflicts) == 2

    def test_filter_conflicts_by_type(self) -> None:
        """Test filtering conflicts by type."""
        skill = SocraticConflictSkill()

        skill.detect_data_conflict(
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        skill.detect_decision_conflict(
            decision_name="d1",
            proposals={"a": "p1", "b": "p2"},
            agents=["a", "b"],
        )

        data_conflicts = skill.list_conflicts(conflict_type="data")
        assert len(data_conflicts) == 1
        assert data_conflicts[0]["conflict"]["conflict_type"] == "data"

    def test_statistics(self) -> None:
        """Test getting statistics."""
        skill = SocraticConflictSkill()

        skill.detect_data_conflict(
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        skill.detect_decision_conflict(
            decision_name="d1",
            proposals={"a": "p1", "b": "p2"},
            agents=["a", "b"],
        )

        stats = skill.get_statistics()

        assert stats["total_conflicts"] == 2
        assert stats["resolved"] == 0
        assert stats["unresolved"] == 2
        assert stats["resolution_rate"] == 0.0

    def test_clear_skill(self) -> None:
        """Test clearing skill state."""
        skill = SocraticConflictSkill()

        skill.detect_data_conflict(
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        assert skill.get_statistics()["total_conflicts"] == 1

        skill.clear()

        assert skill.get_statistics()["total_conflicts"] == 0
