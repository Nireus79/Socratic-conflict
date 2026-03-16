"""Integration tests for LangChain tool."""

from socratic_conflict.integrations.langchain import ConflictResolutionTool


class TestConflictResolutionTool:
    """Test ConflictResolutionTool LangChain integration."""

    def test_tool_creation(self) -> None:
        """Test creating the tool."""
        tool = ConflictResolutionTool()
        assert tool.tool_name == "conflict_resolver"
        assert tool.tool_description is not None

    def test_detect_data_conflict(self) -> None:
        """Test detecting data conflicts."""
        tool = ConflictResolutionTool()

        result = tool.detect_conflict(
            "data",
            field_name="priority",
            values={"agent1": "high", "agent2": "low"},
            agents=["agent1", "agent2"],
        )

        assert result is not None
        assert "conflict_id" in result
        assert result["type"] == "data"

    def test_detect_decision_conflict(self) -> None:
        """Test detecting decision conflicts."""
        tool = ConflictResolutionTool()

        result = tool.detect_conflict(
            "decision",
            decision_name="routing",
            proposals={"agent1": "Path A", "agent2": "Path B"},
            agents=["agent1", "agent2"],
        )

        assert result is not None
        assert result["type"] == "decision"

    def test_detect_workflow_conflict(self) -> None:
        """Test detecting workflow conflicts."""
        tool = ConflictResolutionTool()

        result = tool.detect_conflict(
            "workflow",
            workflow_id="pipeline",
            conflicting_steps=[
                {"step_id": "s1", "agent": "a1", "action": "process"},
                {"step_id": "s2", "agent": "a2", "action": "skip"},
            ],
        )

        assert result is not None
        assert result["type"] == "workflow"

    def test_resolve_conflict(self) -> None:
        """Test resolving a conflict."""
        tool = ConflictResolutionTool()

        # Detect first
        detect_result = tool.detect_conflict(
            "data",
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = detect_result["conflict_id"]

        # Resolve
        result = tool.resolve_conflict(conflict_id, strategy="voting")

        assert result is not None
        assert "recommended_proposal" in result
        assert result["strategy"] == "voting"

    def test_resolve_with_weighted_strategy(self) -> None:
        """Test resolving with weighted strategy."""
        tool = ConflictResolutionTool()

        detect_result = tool.detect_conflict(
            "data",
            field_name="value",
            values={"expert": "x", "junior": "y"},
            agents=["expert", "junior"],
        )
        conflict_id = detect_result["conflict_id"]

        result = tool.resolve_conflict(
            conflict_id,
            strategy="weighted",
            strategy_config={"weights": {"expert": 0.8, "junior": 0.3}},
        )

        assert result is not None
        assert result["strategy"] == "weighted"

    def test_resolve_with_priority_strategy(self) -> None:
        """Test resolving with priority strategy."""
        tool = ConflictResolutionTool()

        detect_result = tool.detect_conflict(
            "decision",
            decision_name="action",
            proposals={"user": "A", "admin": "B"},
            agents=["user", "admin"],
        )
        conflict_id = detect_result["conflict_id"]

        result = tool.resolve_conflict(
            conflict_id,
            strategy="priority",
            strategy_config={"priority_rules": {"admin": 10, "user": 1}},
        )

        assert result is not None
        assert result["strategy"] == "priority"

    def test_record_decision(self) -> None:
        """Test recording a decision."""
        tool = ConflictResolutionTool()

        detect_result = tool.detect_conflict(
            "data",
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = detect_result["conflict_id"]

        result = tool.record_decision(
            conflict_id=conflict_id,
            chosen_proposal_id="p1",
            decided_by="langchain",
        )

        assert result is not None
        assert result["status"] == "recorded"

    def test_get_conflict_details(self) -> None:
        """Test getting conflict details."""
        tool = ConflictResolutionTool()

        detect_result = tool.detect_conflict(
            "data",
            field_name="value",
            values={"a1": "x", "a2": "y"},
            agents=["a1", "a2"],
        )
        conflict_id = detect_result["conflict_id"]

        details = tool.get_conflict_details(conflict_id)

        assert details is not None
        assert details["conflict_id"] == conflict_id
        assert details["resolved"] is False

    def test_get_statistics(self) -> None:
        """Test getting statistics."""
        tool = ConflictResolutionTool()

        # Add conflicts
        tool.detect_conflict(
            "data",
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        tool.detect_conflict(
            "decision",
            decision_name="d1",
            proposals={"a": "p1", "b": "p2"},
            agents=["a", "b"],
        )

        stats = tool.get_statistics()

        assert stats["total_conflicts"] == 2
        assert stats["resolved"] == 0
        assert stats["unresolved"] == 2

    def test_invoke_detect_action(self) -> None:
        """Test invoking detect action."""
        tool = ConflictResolutionTool()

        result = tool.invoke(
            {
                "action": "detect",
                "params": {
                    "conflict_type": "data",
                    "field_name": "value",
                    "values": {"a": "x", "b": "y"},
                    "agents": ["a", "b"],
                },
            }
        )

        assert result is not None
        assert result["type"] == "data"

    def test_invoke_resolve_action(self) -> None:
        """Test invoking resolve action."""
        tool = ConflictResolutionTool()

        # First detect
        detect_result = tool.invoke(
            {
                "action": "detect",
                "params": {
                    "conflict_type": "data",
                    "field_name": "value",
                    "values": {"a": "x", "b": "y"},
                    "agents": ["a", "b"],
                },
            }
        )
        conflict_id = detect_result["conflict_id"]

        # Then resolve
        result = tool.invoke(
            {
                "action": "resolve",
                "params": {
                    "conflict_id": conflict_id,
                    "strategy": "voting",
                },
            }
        )

        assert result is not None
        assert "recommended_proposal" in result

    def test_invoke_statistics_action(self) -> None:
        """Test invoking statistics action."""
        tool = ConflictResolutionTool()

        # Add conflict
        tool.detect_conflict(
            "data",
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        result = tool.invoke({"action": "statistics", "params": {}})

        assert result["total_conflicts"] == 1

    def test_invoke_invalid_action(self) -> None:
        """Test invoking invalid action."""
        tool = ConflictResolutionTool()

        result = tool.invoke({"action": "invalid", "params": {}})

        assert "error" in result

    def test_clear_tool(self) -> None:
        """Test clearing tool state."""
        tool = ConflictResolutionTool()

        tool.detect_conflict(
            "data",
            field_name="f1",
            values={"a": "x", "b": "y"},
            agents=["a", "b"],
        )

        assert tool.get_statistics()["total_conflicts"] == 1

        tool.clear()

        assert tool.get_statistics()["total_conflicts"] == 0
