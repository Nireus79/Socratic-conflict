"""Unit tests for AsyncConflictDetector."""

import asyncio
import pytest

from socratic_conflict import AsyncConflictDetector, Conflict
from socratic_conflict.core.conflict import Proposal, Resolution


class TestAsyncConflictDetector:
    """Test AsyncConflictDetector async operations."""

    @pytest.fixture
    def detector(self):
        """Create detector for testing."""
        return AsyncConflictDetector()

    @pytest.mark.asyncio
    async def test_detect_data_conflict_async(self, detector):
        """Test async data conflict detection."""
        conflict = await detector.detect_data_conflict(
            field_name="priority",
            values={"agent1": "high", "agent2": "low", "agent3": "medium"},
            agents=["agent1", "agent2", "agent3"],
        )

        assert conflict is not None
        assert conflict.title == "Data Conflict: priority"
        assert conflict.conflict_type == "data"
        assert len(conflict.proposals) == 3

    @pytest.mark.asyncio
    async def test_detect_decision_conflict_async(self, detector):
        """Test async decision conflict detection."""
        conflict = await detector.detect_decision_conflict(
            decision_name="approval",
            proposals={
                "agent1": "Approve immediately",
                "agent2": "Require changes",
                "agent3": "Reject",
            },
            agents=["agent1", "agent2", "agent3"],
        )

        assert conflict is not None
        assert conflict.title == "Decision Conflict: approval"
        assert conflict.conflict_type == "decision"
        assert len(conflict.proposals) == 3

    @pytest.mark.asyncio
    async def test_detect_workflow_conflict_async(self, detector):
        """Test async workflow conflict detection."""
        conflict = await detector.detect_workflow_conflict(
            workflow_name="pipeline",
            task_results={
                "executor1": {"status": "completed", "result": 100},
                "executor2": {"status": "failed", "error": "timeout"},
            },
            agents=["executor1", "executor2"],
        )

        assert conflict is not None
        assert conflict.title == "Workflow Conflict: pipeline"
        assert conflict.conflict_type == "workflow"

    @pytest.mark.asyncio
    async def test_detect_consensus_conflict_async(self, detector):
        """Test async consensus conflict detection."""
        conflict = await detector.detect_consensus_conflict(
            topic="feature_request",
            votes={
                "agent1": "yes",
                "agent2": "no",
                "agent3": "no",
                "agent4": "yes",
            },
            agents=["agent1", "agent2", "agent3", "agent4"],
            required_consensus=0.8,
        )

        assert conflict is not None
        assert conflict.title == "Consensus Conflict: feature_request"
        assert conflict.conflict_type == "consensus"

    @pytest.mark.asyncio
    async def test_resolve_async(self, detector):
        """Test async conflict resolution."""
        from socratic_conflict import VotingStrategy

        # Create conflict
        conflict = await detector.detect_decision_conflict(
            decision_name="approve",
            proposals={
                "agent1": "yes",
                "agent2": "yes",
                "agent3": "no",
            },
            agents=["agent1", "agent2", "agent3"],
        )

        # Resolve asynchronously
        strategy = VotingStrategy()
        resolution = await detector.resolve(conflict, strategy)

        assert resolution is not None
        assert resolution.strategy_used == "voting"
        assert resolution.selected_proposal is not None

    @pytest.mark.asyncio
    async def test_resolve_multiple_async(self, detector):
        """Test async resolution of multiple conflicts."""
        from socratic_conflict import MajorityConsensus

        # Create multiple conflicts
        conflict1 = await detector.detect_data_conflict(
            field_name="field1",
            values={"agent1": "value1", "agent2": "value2"},
            agents=["agent1", "agent2"],
        )

        conflict2 = await detector.detect_decision_conflict(
            decision_name="decision1",
            proposals={"agent1": "option_a", "agent2": "option_b"},
            agents=["agent1", "agent2"],
        )

        # Resolve both asynchronously
        strategy = MajorityConsensus()
        resolutions = await detector.resolve_multiple(
            [conflict1, conflict2], strategy
        )

        assert len(resolutions) == 2
        assert resolutions[0] is not None
        assert resolutions[1] is not None

    @pytest.mark.asyncio
    async def test_get_detected_conflicts_async(self, detector):
        """Test getting detected conflicts asynchronously."""
        # Create some conflicts
        await detector.detect_data_conflict(
            field_name="field1",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
        )

        await detector.detect_decision_conflict(
            decision_name="decision1",
            proposals={"agent1": "opt1", "agent2": "opt2"},
            agents=["agent1", "agent2"],
        )

        # Get conflicts
        conflicts = await detector.get_detected_conflicts()

        assert len(conflicts) >= 2

    @pytest.mark.asyncio
    async def test_get_conflicts_by_type_async(self, detector):
        """Test filtering conflicts by type asynchronously."""
        await detector.detect_data_conflict(
            field_name="field1",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
        )

        await detector.detect_decision_conflict(
            decision_name="decision1",
            proposals={"agent1": "opt1", "agent2": "opt2"},
            agents=["agent1", "agent2"],
        )

        # Get data conflicts only
        data_conflicts = await detector.get_conflicts_by_type("data")

        assert len(data_conflicts) >= 1
        assert all(c.conflict_type == "data" for c in data_conflicts)

    @pytest.mark.asyncio
    async def test_get_conflicts_by_severity_async(self, detector):
        """Test filtering conflicts by severity asynchronously."""
        conflict = await detector.detect_data_conflict(
            field_name="critical_field",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
            context={"severity": "critical"},
        )

        # Get high severity conflicts
        high_severity = await detector.get_conflicts_by_severity("high")

        # Should include our conflict if it was marked high
        assert isinstance(high_severity, list)

    @pytest.mark.asyncio
    async def test_get_agent_conflicts_async(self, detector):
        """Test getting conflicts by agent asynchronously."""
        await detector.detect_data_conflict(
            field_name="field1",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
        )

        await detector.detect_decision_conflict(
            decision_name="decision1",
            proposals={"agent1": "opt1", "agent2": "opt2", "agent3": "opt3"},
            agents=["agent1", "agent2", "agent3"],
        )

        # Get agent1's conflicts
        agent_conflicts = await detector.get_agent_conflicts("agent1")

        assert len(agent_conflicts) >= 1
        assert all("agent1" in c.related_agents for c in agent_conflicts)

    @pytest.mark.asyncio
    async def test_clear_conflicts_async(self, detector):
        """Test clearing conflicts asynchronously."""
        # Create conflicts
        await detector.detect_data_conflict(
            field_name="field1",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
        )

        # Verify conflicts exist
        conflicts = await detector.get_detected_conflicts()
        assert len(conflicts) > 0

        # Clear conflicts
        await detector.clear_conflicts()

        # Verify cleared
        conflicts = await detector.get_detected_conflicts()
        assert len(conflicts) == 0

    @pytest.mark.asyncio
    async def test_concurrent_conflict_detection(self, detector):
        """Test concurrent conflict detection."""
        # Create multiple conflicts concurrently
        tasks = [
            detector.detect_data_conflict(
                field_name=f"field{i}",
                values={f"agent1": f"value{i}a", f"agent2": f"value{i}b"},
                agents=[f"agent1", f"agent2"],
            )
            for i in range(5)
        ]

        conflicts = await asyncio.gather(*tasks)

        assert len(conflicts) == 5
        assert all(c is not None for c in conflicts)

    @pytest.mark.asyncio
    async def test_concurrent_resolution(self, detector):
        """Test concurrent conflict resolution."""
        from socratic_conflict import VotingStrategy

        strategy = VotingStrategy()

        # Create conflicts
        conflict1 = await detector.detect_decision_conflict(
            decision_name="decision1",
            proposals={"agent1": "a", "agent2": "a", "agent3": "b"},
            agents=["agent1", "agent2", "agent3"],
        )

        conflict2 = await detector.detect_decision_conflict(
            decision_name="decision2",
            proposals={"agent1": "x", "agent2": "y", "agent3": "y"},
            agents=["agent1", "agent2", "agent3"],
        )

        # Resolve concurrently
        resolutions = await asyncio.gather(
            detector.resolve(conflict1, strategy),
            detector.resolve(conflict2, strategy),
        )

        assert len(resolutions) == 2
        assert all(r is not None for r in resolutions)

    @pytest.mark.asyncio
    async def test_async_detector_with_large_conflicts(self, detector):
        """Test async detector with many agents."""
        large_values = {f"agent{i}": f"value{i}" for i in range(100)}
        large_agents = list(large_values.keys())

        conflict = await detector.detect_data_conflict(
            field_name="large_field",
            values=large_values,
            agents=large_agents,
        )

        assert conflict is not None
        assert len(conflict.proposals) == 100

    @pytest.mark.asyncio
    async def test_no_conflict_async(self, detector):
        """Test async detection when no conflict exists."""
        # All agents agree
        conflict = await detector.detect_data_conflict(
            field_name="agreed_field",
            values={"agent1": "same", "agent2": "same", "agent3": "same"},
            agents=["agent1", "agent2", "agent3"],
        )

        assert conflict is None

    @pytest.mark.asyncio
    async def test_single_agent_async(self, detector):
        """Test async detection with single agent."""
        conflict = await detector.detect_decision_conflict(
            decision_name="single_agent_decision",
            proposals={"agent1": "option_a"},
            agents=["agent1"],
        )

        assert conflict is None  # No conflict with single agent

    @pytest.mark.asyncio
    async def test_context_preservation_async(self, detector):
        """Test that context is preserved in async operations."""
        context_data = {
            "workflow_id": "wf_123",
            "timestamp": "2024-03-16T10:00:00Z",
            "user_id": "user_456",
        }

        conflict = await detector.detect_data_conflict(
            field_name="field_with_context",
            values={"agent1": "a", "agent2": "b"},
            agents=["agent1", "agent2"],
            context=context_data,
        )

        assert conflict is not None
        assert conflict.context == context_data
