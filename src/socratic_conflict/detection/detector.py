"""Conflict detection engine for identifying disagreements and conflicts."""

from typing import Any, Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, Proposal


class ConflictDetector:
    """Detects conflicts in data, decisions, and workflows."""

    def __init__(self):
        """Initialize conflict detector."""
        self.detected_conflicts: List[Conflict] = []

    def detect_data_conflict(
        self,
        field_name: str,
        values: Dict[str, Any],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in data values from different sources.

        Args:
            field_name: Name of the field with conflicting values
            values: Dict mapping agent_name to their proposed value
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        if len(set(str(v) for v in values.values())) <= 1:
            return None  # No conflict

        conflict = Conflict(
            title=f"Data Conflict: {field_name}",
            description=f"Agents have conflicting values for {field_name}",
            conflict_type="data",
            severity=self._calculate_severity(values),
            related_agents=agents,
            context=context or {},
        )

        # Create proposals for each agent's value
        for agent, value in values.items():
            proposal = Proposal(
                title=f"{agent}'s value for {field_name}",
                description=f"{field_name} = {value}",
                source_agent=agent,
                confidence=0.5,  # Base confidence
            )
            conflict.proposals.append(proposal)

        self.detected_conflicts.append(conflict)
        return conflict

    def detect_decision_conflict(
        self,
        decision_name: str,
        proposals: Dict[str, str],  # agent -> rationale
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in decision-making between agents.

        Args:
            decision_name: Name of the decision
            proposals: Dict mapping agent_name to their proposal/rationale
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        if len(proposals) <= 1:
            return None  # No conflict

        conflict = Conflict(
            title=f"Decision Conflict: {decision_name}",
            description=f"Agents disagree on {decision_name}",
            conflict_type="decision",
            severity="high",
            related_agents=agents,
            context=context or {},
        )

        # Create proposals
        for agent, rationale in proposals.items():
            proposal = Proposal(
                title=f"{agent}'s proposal for {decision_name}",
                description=rationale,
                source_agent=agent,
                rationale=rationale,
                confidence=0.7,
            )
            conflict.proposals.append(proposal)

        self.detected_conflicts.append(conflict)
        return conflict

    def detect_workflow_conflict(
        self,
        workflow_id: str,
        conflicting_steps: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in workflow execution.

        Args:
            workflow_id: ID of the workflow
            conflicting_steps: Steps that are in conflict
            context: Additional context

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        if len(conflicting_steps) <= 1:
            return None

        conflict = Conflict(
            title=f"Workflow Conflict: {workflow_id}",
            description="Multiple workflow execution paths are conflicting",
            conflict_type="workflow",
            severity="high",
            related_agents=[step.get("agent", "unknown") for step in conflicting_steps],
            context=context or {},
        )

        for step in conflicting_steps:
            proposal = Proposal(
                title=f"Step {step.get('step_id', 'unknown')}",
                description=f"Execute: {step.get('action', 'unknown')}",
                source_agent=step.get("agent", "unknown"),
                confidence=step.get("confidence", 0.5),
            )
            conflict.proposals.append(proposal)

        self.detected_conflicts.append(conflict)
        return conflict

    def get_conflicts(self, conflict_type: Optional[str] = None) -> List[Conflict]:
        """Get detected conflicts, optionally filtered by type.

        Args:
            conflict_type: Optional type filter (data, decision, workflow, consensus)

        Returns:
            List of Conflict objects
        """
        if conflict_type:
            return [c for c in self.detected_conflicts if c.conflict_type == conflict_type]
        return self.detected_conflicts

    def get_conflict(self, conflict_id: str) -> Optional[Conflict]:
        """Get a specific conflict by ID.

        Args:
            conflict_id: ID of the conflict

        Returns:
            Conflict object or None if not found
        """
        for conflict in self.detected_conflicts:
            if conflict.conflict_id == conflict_id:
                return conflict
        return None

    def clear_conflicts(self) -> None:
        """Clear all detected conflicts."""
        self.detected_conflicts = []

    @staticmethod
    def _calculate_severity(values: Dict[str, Any]) -> str:
        """Calculate severity based on value differences.

        Args:
            values: Dict of values to compare

        Returns:
            Severity level (low, medium, high, critical)
        """
        # Placeholder logic - can be enhanced
        if len(values) >= 3:
            return "high"
        return "medium"
