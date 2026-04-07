"""Conflict history tracking and versioning."""

from typing import Any, Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, ConflictDecision, Resolution


class HistoryTracker:
    """Tracks conflicts and decisions over time with versioning."""

    def __init__(self):
        """Initialize history tracker."""
        self._conflicts: Dict[str, Conflict] = {}
        self._resolutions: Dict[str, Resolution] = {}
        self._decisions: Dict[str, List[ConflictDecision]] = {}

    @property
    def conflict_history(self) -> Dict[str, Conflict]:
        """Get conflict history as dict indexed by conflict_id."""
        return self._conflicts

    @property
    def resolution_history(self) -> Dict[str, Resolution]:
        """Get resolution history as dict indexed by resolution_id."""
        return self._resolutions

    @property
    def decision_history(self) -> Dict[str, List[ConflictDecision]]:
        """Get decision history as dict indexed by conflict_id."""
        return self._decisions

    def add_conflict(self, conflict: Conflict) -> None:
        """Add a conflict to history.

        Args:
            conflict: Conflict to track
        """
        self._conflicts[conflict.conflict_id] = conflict

    def add_resolution(self, resolution: Resolution) -> None:
        """Add a resolution attempt to history.

        Args:
            resolution: Resolution to track
        """
        self._resolutions[resolution.resolution_id] = resolution

    def add_decision(self, decision: ConflictDecision) -> None:
        """Add a final decision to history.

        Args:
            decision: Decision to track
        """
        conflict_id = decision.conflict_id
        if conflict_id not in self._decisions:
            self._decisions[conflict_id] = []
        self._decisions[conflict_id].append(decision)

    def get_conflict_history(self, conflict_id: str) -> Dict[str, Any]:
        """Get complete history for a specific conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            Dict with conflicts, resolutions, and decisions lists
        """
        conflict = self._conflicts.get(conflict_id)
        conflicts_list = [conflict] if conflict else []

        related_resolutions = [
            r for r in self._resolutions.values()
            if r.conflict_id == conflict_id
        ]

        related_decisions = self._decisions.get(conflict_id, [])

        return {
            "conflicts": conflicts_list,
            "resolutions": related_resolutions,
            "decisions": related_decisions,
        }

    def get_agent_conflict_history(self, agent_name: str) -> List[Conflict]:
        """Get conflict history for a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of conflicts involving this agent
        """
        return [
            c for c in self._conflicts.values()
            if agent_name in c.related_agents
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about conflict history.

        Returns:
            Dict with conflict statistics
        """
        total_conflicts = len(self._conflicts)
        resolved_count = len(self._decisions)  # Number of conflicts with decisions

        by_type: Dict[str, int] = {}
        for conflict in self._conflicts.values():
            by_type[conflict.conflict_type] = by_type.get(conflict.conflict_type, 0) + 1

        by_severity: Dict[str, int] = {}
        for conflict in self._conflicts.values():
            by_severity[conflict.severity] = by_severity.get(conflict.severity, 0) + 1

        total_resolutions = len(self._resolutions)
        resolution_rate = (
            (total_resolutions / total_conflicts * 100)
            if total_conflicts > 0
            else 0
        )

        return {
            "total_conflicts": total_conflicts,
            "resolved_count": resolved_count,
            "by_type": by_type,
            "by_severity": by_severity,
            "total_resolutions": total_resolutions,
            "resolution_rate": resolution_rate,
        }

    def get_decision_versions(self, conflict_id: str) -> List[ConflictDecision]:
        """Get all versions/revisions of decisions for a conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            List of ConflictDecision objects sorted by version
        """
        decisions = self._decisions.get(conflict_id, [])
        return sorted(decisions, key=lambda d: d.version)

    def revert_decision(self, conflict_id: str, new_decision: ConflictDecision) -> None:
        """Add a new decision version for a conflict.

        Args:
            conflict_id: ID of the conflict
            new_decision: New ConflictDecision to add
        """
        if conflict_id not in self._decisions:
            self._decisions[conflict_id] = []

        # Set version to next available
        current_versions = self._decisions.get(conflict_id, [])
        max_version = max((d.version for d in current_versions), default=0)
        new_decision.version = max_version + 1

        self._decisions[conflict_id].append(new_decision)

    def clear_history(self) -> Dict[str, int]:
        """Clear all history and return statistics.

        Returns:
            Dict with count of cleared items
        """
        cleared = {
            "cleared_conflicts": len(self._conflicts),
            "cleared_resolutions": len(self._resolutions),
            "cleared_decisions": sum(len(d) for d in self._decisions.values()),
        }

        self._conflicts = {}
        self._resolutions = {}
        self._decisions = {}

        return cleared
