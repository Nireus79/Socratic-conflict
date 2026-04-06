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

    def detect_consensus_conflict(
        self,
        proposals: List[Proposal],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts when agents cannot reach consensus.

        Args:
            proposals: List of proposals from different agents
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if consensus conflict detected, None otherwise
        """
        if len(set(p.title for p in proposals)) <= 1:
            return None  # All agree on same proposal

        conflict = Conflict(
            title="Consensus Conflict",
            description="Agents cannot reach consensus",
            conflict_type="consensus",
            severity="high",
            related_agents=agents,
            proposals=proposals,
            context=context or {},
        )

        self.detected_conflicts.append(conflict)
        return conflict

    def get_conflicts_by_type(self, conflict_type: str) -> List[Conflict]:
        """Get all conflicts of a specific type.

        Args:
            conflict_type: Type of conflict to filter by

        Returns:
            List of conflicts of that type
        """
        return [c for c in self.detected_conflicts if c.conflict_type == conflict_type]

    def get_conflicts_by_severity(self, severity: str) -> List[Conflict]:
        """Get all conflicts of a specific severity level.

        Args:
            severity: Severity level to filter by (low, medium, high, critical)

        Returns:
            List of conflicts with that severity
        """
        return [c for c in self.detected_conflicts if c.severity == severity]

    def get_agent_conflicts(self, agent_name: str) -> List[Conflict]:
        """Get all conflicts involving a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of conflicts involving that agent
        """
        return [c for c in self.detected_conflicts if agent_name in c.related_agents]

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
