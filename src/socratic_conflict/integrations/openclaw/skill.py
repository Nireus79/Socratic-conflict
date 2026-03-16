"""Openclaw skill integration for Socratic Conflict."""

from typing import Any, Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, ConflictDecision, Resolution
from socratic_conflict.detection.detector import ConflictDetector
from socratic_conflict.resolution.strategies import (
    ConsensusStrategy,
    HybridStrategy,
    PriorityStrategy,
    ResolutionStrategy,
    VotingStrategy,
    WeightedStrategy,
)


class SocraticConflictSkill:
    """Openclaw skill for conflict detection and resolution.

    Provides automated conflict detection and resolution capabilities
    for multi-agent systems in Openclaw workflows.
    """

    def __init__(self) -> None:
        """Initialize the Socratic Conflict skill."""
        self.detector = ConflictDetector()
        self._conflicts: Dict[str, Conflict] = {}
        self._resolutions: Dict[str, Resolution] = {}
        self._decisions: Dict[str, ConflictDecision] = {}

    def detect_data_conflict(
        self,
        field_name: str,
        values: Dict[str, Any],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Detect data conflicts among agent proposals.

        Args:
            field_name: Name of the field with conflicting values
            values: Dictionary mapping agent names to their proposed values
            agents: List of agent names involved
            context: Optional context information

        Returns:
            Conflict details as dict, or None if no conflict detected
        """
        conflict = self.detector.detect_data_conflict(
            field_name=field_name,
            values=values,
            agents=agents,
            context=context or {},
        )

        if conflict:
            self._conflicts[conflict.conflict_id] = conflict
            return conflict.to_dict()

        return None

    def detect_decision_conflict(
        self,
        decision_name: str,
        proposals: Dict[str, str],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Detect decision conflicts among agents.

        Args:
            decision_name: Name of the decision being made
            proposals: Dictionary mapping agent names to their proposals
            agents: List of agent names involved
            context: Optional context information

        Returns:
            Conflict details as dict, or None if no conflict detected
        """
        conflict = self.detector.detect_decision_conflict(
            decision_name=decision_name,
            proposals=proposals,
            agents=agents,
            context=context or {},
        )

        if conflict:
            self._conflicts[conflict.conflict_id] = conflict
            return conflict.to_dict()

        return None

    def detect_workflow_conflict(
        self,
        workflow_id: str,
        conflicting_steps: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Detect workflow execution conflicts.

        Args:
            workflow_id: ID of the workflow
            conflicting_steps: List of conflicting step definitions
            context: Optional context information

        Returns:
            Conflict details as dict, or None if no conflict detected
        """
        conflict = self.detector.detect_workflow_conflict(
            workflow_id=workflow_id,
            conflicting_steps=conflicting_steps,
            context=context or {},
        )

        if conflict:
            self._conflicts[conflict.conflict_id] = conflict
            return conflict.to_dict()

        return None

    def resolve_with_strategy(
        self,
        conflict_id: str,
        strategy: str = "voting",
        strategy_config: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Resolve a conflict using specified strategy.

        Args:
            conflict_id: ID of the conflict to resolve
            strategy: Strategy name (voting, consensus, weighted, priority, hybrid)
            strategy_config: Optional configuration for the strategy

        Returns:
            Resolution details as dict, or None if conflict not found
        """
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            return None

        resolver: Optional[ResolutionStrategy] = None

        if strategy == "voting":
            resolver = VotingStrategy()
        elif strategy == "consensus":
            resolver = ConsensusStrategy()
        elif strategy == "weighted":
            weights = strategy_config.get("weights", {}) if strategy_config else {}
            resolver = WeightedStrategy(weights=weights)
        elif strategy == "priority":
            rules = strategy_config.get("priority_rules", {}) if strategy_config else {}
            resolver = PriorityStrategy(priority_rules=rules)
        elif strategy == "hybrid":
            strategies_names = strategy_config.get("strategies", []) if strategy_config else []
            strategies: List[ResolutionStrategy] = []

            for strat_name in strategies_names:
                if strat_name == "voting":
                    strategies.append(VotingStrategy())
                elif strat_name == "consensus":
                    strategies.append(ConsensusStrategy())
                elif strat_name == "weighted":
                    weights = strategy_config.get("weights", {}) if strategy_config else {}
                    strategies.append(WeightedStrategy(weights=weights))
                elif strat_name == "priority":
                    rules = strategy_config.get("priority_rules", {}) if strategy_config else {}
                    strategies.append(PriorityStrategy(priority_rules=rules))

            if strategies:
                resolver = HybridStrategy(strategies=strategies)

        if not resolver:
            return None

        resolution = resolver.resolve(conflict)
        if resolution:
            self._resolutions[conflict_id] = resolution
            return resolution.to_dict()

        return None

    def make_decision(
        self,
        conflict_id: str,
        chosen_proposal_id: str,
        decided_by: str = "skill",
        reason: str = "",
    ) -> Dict[str, Any]:
        """Record a final decision on a conflict.

        Args:
            conflict_id: ID of the conflict
            chosen_proposal_id: ID of chosen proposal
            decided_by: Who made the decision (agent/user name)
            reason: Reason for the decision

        Returns:
            Decision details as dict
        """
        decision = ConflictDecision(
            conflict_id=conflict_id,
            chosen_proposal_id=chosen_proposal_id,
            decided_by=decided_by,
        )

        self._decisions[conflict_id] = decision
        return decision.to_dict()

    def get_conflict_summary(self, conflict_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            Conflict summary dict, or None if not found
        """
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            return None

        resolution = self._resolutions.get(conflict_id)
        decision = self._decisions.get(conflict_id)

        return {
            "conflict": conflict.to_dict(),
            "resolution": resolution.to_dict() if resolution else None,
            "decision": decision.to_dict() if decision else None,
            "status": "resolved" if decision else "unresolved",
        }

    def list_conflicts(
        self,
        conflict_type: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List all detected conflicts.

        Args:
            conflict_type: Filter by conflict type (data, decision, workflow)
            severity: Filter by severity (low, medium, high, critical)

        Returns:
            List of conflict summaries
        """
        conflicts = []

        for conflict in self._conflicts.values():
            if conflict_type and conflict.conflict_type != conflict_type:
                continue
            if severity and conflict.severity != severity:
                continue

            summary = self.get_conflict_summary(conflict.conflict_id)
            if summary:
                conflicts.append(summary)

        return conflicts

    def get_statistics(self) -> Dict[str, Any]:
        """Get conflict statistics.

        Returns:
            Dictionary with conflict statistics
        """
        total_conflicts = len(self._conflicts)
        resolved_conflicts = len(self._decisions)
        unresolved_conflicts = total_conflicts - resolved_conflicts

        conflict_types: Dict[str, int] = {}
        severity_levels: Dict[str, int] = {}

        for conflict in self._conflicts.values():
            conflict_types[conflict.conflict_type] = (
                conflict_types.get(conflict.conflict_type, 0) + 1
            )
            severity_levels[conflict.severity] = severity_levels.get(conflict.severity, 0) + 1

        resolution_strategies: Dict[str, int] = {}

        for resolution in self._resolutions.values():
            resolution_strategies[resolution.strategy] = (
                resolution_strategies.get(resolution.strategy, 0) + 1
            )

        return {
            "total_conflicts": total_conflicts,
            "resolved": resolved_conflicts,
            "unresolved": unresolved_conflicts,
            "resolution_rate": (
                resolved_conflicts / total_conflicts if total_conflicts > 0 else 0.0
            ),
            "conflict_types": conflict_types,
            "severity_levels": severity_levels,
            "resolution_strategies": resolution_strategies,
        }

    def clear(self) -> None:
        """Clear all tracked conflicts, resolutions, and decisions."""
        self._conflicts.clear()
        self._resolutions.clear()
        self._decisions.clear()
        self.detector.clear_conflicts()
