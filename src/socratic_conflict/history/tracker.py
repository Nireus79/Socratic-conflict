"""Conflict history tracking and versioning."""

from typing import Any, Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, ConflictDecision, Resolution


class HistoryTracker:
    """Tracks conflicts and decisions over time with versioning."""

    def __init__(self):
        """Initialize history tracker."""
        self.conflicts: List[Conflict] = []
        self.resolutions: List[Resolution] = []
        self.decisions: List[ConflictDecision] = []

    def add_conflict(self, conflict: Conflict) -> None:
        """Add a conflict to history.

        Args:
            conflict: Conflict to track
        """
        self.conflicts.append(conflict)

    def add_resolution(self, resolution: Resolution) -> None:
        """Add a resolution attempt to history.

        Args:
            resolution: Resolution to track
        """
        self.resolutions.append(resolution)

    def add_decision(self, decision: ConflictDecision) -> None:
        """Add a final decision to history.

        Args:
            decision: Decision to track
        """
        self.decisions.append(decision)

    def get_conflict_history(self, conflict_id: str) -> Dict[str, Any]:
        """Get complete history for a specific conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            Dict with conflict, resolutions, and final decision
        """
        conflict = next(
            (c for c in self.conflicts if c.conflict_id == conflict_id), None
        )
        if not conflict:
            return {}

        related_resolutions = [
            r for r in self.resolutions if r.conflict_id == conflict_id
        ]
        final_decision = next(
            (d for d in self.decisions if d.conflict_id == conflict_id), None
        )

        return {
            "conflict": conflict.to_dict(),
            "resolutions": [r.to_dict() for r in related_resolutions],
            "final_decision": final_decision.to_dict() if final_decision else None,
        }

    def get_agent_conflict_history(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get conflict history for a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of conflicts involving this agent
        """
        agent_conflicts = [
            c for c in self.conflicts if agent_name in c.related_agents
        ]

        history = []
        for conflict in agent_conflicts:
            history.append(self.get_conflict_history(conflict.conflict_id))

        return history

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about conflict history.

        Returns:
            Dict with conflict statistics
        """
        total_conflicts = len(self.conflicts)
        resolved = len([d for d in self.decisions if d.conflict_id])
        unresolved = total_conflicts - resolved

        conflict_types: Dict[str, int] = {}
        for conflict in self.conflicts:
            conflict_types[conflict.conflict_type] = (
                conflict_types.get(conflict.conflict_type, 0) + 1
            )

        severity_counts: Dict[str, int] = {}
        for conflict in self.conflicts:
            severity_counts[conflict.severity] = (
                severity_counts.get(conflict.severity, 0) + 1
            )

        strategies_used: Dict[str, int] = {}
        for resolution in self.resolutions:
            strategies_used[resolution.strategy] = (
                strategies_used.get(resolution.strategy, 0) + 1
            )

        return {
            "total_conflicts": total_conflicts,
            "resolved": resolved,
            "unresolved": unresolved,
            "resolution_rate": resolved / total_conflicts if total_conflicts > 0 else 0,
            "conflict_types": conflict_types,
            "severities": severity_counts,
            "strategies_used": strategies_used,
            "total_resolutions_attempted": len(self.resolutions),
            "total_decisions": len(self.decisions),
        }

    def get_decision_versions(self, conflict_id: str) -> List[ConflictDecision]:
        """Get all versions/revisions of decisions for a conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            List of ConflictDecision objects sorted by version
        """
        versions = [
            d for d in self.decisions if d.conflict_id == conflict_id
        ]
        return sorted(versions, key=lambda d: d.version)

    def revert_decision(self, decision_id: str, reason: str) -> Optional[ConflictDecision]:
        """Create a new decision version reverting to a previous decision.

        Args:
            decision_id: ID of decision to revert
            reason: Reason for reverting

        Returns:
            New ConflictDecision with reverted state or None
        """
        original = next((d for d in self.decisions if d.decision_id == decision_id), None)
        if not original:
            return None

        new_decision = ConflictDecision(
            conflict_id=original.conflict_id,
            resolution_id=original.resolution_id,
            chosen_proposal_id=original.chosen_proposal_id,
            decided_by="system_revert",
            rationale=f"Reverted: {reason}",
            version=original.version + 1,
        )

        self.add_decision(new_decision)
        return new_decision

    def clear_history(self) -> None:
        """Clear all history (use with caution)."""
        self.conflicts = []
        self.resolutions = []
        self.decisions = []
