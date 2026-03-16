"""LangChain tool integration for Socratic Conflict."""

from typing import Any, Dict, List, Optional, Union

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


class ConflictResolutionTool:
    """LangChain tool for conflict detection and resolution.

    Can be used in LangChain chains and agents to automatically detect
    and resolve conflicts in multi-agent conversations and workflows.
    """

    def __init__(self) -> None:
        """Initialize the Conflict Resolution Tool."""
        self.detector = ConflictDetector()
        self._conflicts: Dict[str, Conflict] = {}
        self._resolutions: Dict[str, Resolution] = {}
        self._decisions: Dict[str, ConflictDecision] = {}

    @property
    def tool_name(self) -> str:
        """Get the tool name for LangChain."""
        return "conflict_resolver"

    @property
    def tool_description(self) -> str:
        """Get the tool description for LangChain."""
        return (
            "Detects and resolves conflicts between multiple agents or proposals. "
            "Can handle data conflicts, decision conflicts, and workflow conflicts. "
            "Supports multiple resolution strategies: voting, consensus, weighted, priority, hybrid."
        )

    def detect_conflict(
        self,
        conflict_type: str,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Detect a conflict of specified type.

        Args:
            conflict_type: Type of conflict (data, decision, workflow)
            **kwargs: Type-specific parameters

        Returns:
            Conflict details as dict, or None if no conflict detected
        """
        if conflict_type == "data":
            field_name = kwargs.get("field_name", "")
            values = kwargs.get("values", {})
            agents = kwargs.get("agents", [])
            context = kwargs.get("context")

            conflict = self.detector.detect_data_conflict(
                field_name=field_name,
                values=values,
                agents=agents,
                context=context or {},
            )

        elif conflict_type == "decision":
            decision_name = kwargs.get("decision_name", "")
            proposals = kwargs.get("proposals", {})
            agents = kwargs.get("agents", [])
            context = kwargs.get("context")

            conflict = self.detector.detect_decision_conflict(
                decision_name=decision_name,
                proposals=proposals,
                agents=agents,
                context=context or {},
            )

        elif conflict_type == "workflow":
            workflow_id = kwargs.get("workflow_id", "")
            conflicting_steps = kwargs.get("conflicting_steps", [])
            context = kwargs.get("context")

            conflict = self.detector.detect_workflow_conflict(
                workflow_id=workflow_id,
                conflicting_steps=conflicting_steps,
                context=context or {},
            )

        else:
            return {"error": f"Unknown conflict type: {conflict_type}"}

        if conflict:
            self._conflicts[conflict.conflict_id] = conflict
            return {
                "conflict_id": conflict.conflict_id,
                "type": conflict.conflict_type,
                "severity": conflict.severity,
                "agents": conflict.related_agents,
                "proposals_count": len(conflict.proposals),
            }

        return None

    def resolve_conflict(
        self,
        conflict_id: str,
        strategy: str = "voting",
        strategy_config: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Resolve a detected conflict using specified strategy.

        Args:
            conflict_id: ID of the conflict to resolve
            strategy: Strategy name (voting, consensus, weighted, priority, hybrid)
            strategy_config: Optional configuration for the strategy

        Returns:
            Resolution details as dict, or None if conflict not found
        """
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            return {"error": f"Conflict {conflict_id} not found"}

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
            return {"error": f"Unknown strategy: {strategy}"}

        resolution = resolver.resolve(conflict)
        if resolution:
            self._resolutions[conflict_id] = resolution
            return {
                "conflict_id": conflict_id,
                "strategy": resolution.strategy,
                "recommended_proposal": resolution.recommended_proposal_id,
                "confidence": f"{resolution.confidence:.2%}",
            }

        return None

    def record_decision(
        self,
        conflict_id: str,
        chosen_proposal_id: str,
        decided_by: str = "langchain_agent",
        reason: str = "",
    ) -> Dict[str, Any]:
        """Record a final decision on a conflict.

        Args:
            conflict_id: ID of the conflict
            chosen_proposal_id: ID of chosen proposal
            decided_by: Who made the decision
            reason: Reason for the decision

        Returns:
            Decision details as dict
        """
        if conflict_id not in self._conflicts:
            return {"error": f"Conflict {conflict_id} not found"}

        decision = ConflictDecision(
            conflict_id=conflict_id,
            chosen_proposal_id=chosen_proposal_id,
            decided_by=decided_by,
        )

        self._decisions[conflict_id] = decision
        return {
            "conflict_id": conflict_id,
            "chosen_proposal": chosen_proposal_id,
            "decided_by": decided_by,
            "status": "recorded",
        }

    def get_conflict_details(self, conflict_id: str) -> Dict[str, Any]:
        """Get detailed information about a conflict.

        Args:
            conflict_id: ID of the conflict

        Returns:
            Conflict details as dict
        """
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            return {"error": f"Conflict {conflict_id} not found"}

        resolution = self._resolutions.get(conflict_id)
        decision = self._decisions.get(conflict_id)

        return {
            "conflict_id": conflict_id,
            "type": conflict.conflict_type,
            "severity": conflict.severity,
            "agents_involved": conflict.related_agents,
            "num_proposals": len(conflict.proposals),
            "resolved": decision is not None,
            "resolution_strategy": resolution.strategy if resolution else None,
            "recommended_proposal": resolution.recommended_proposal_id if resolution else None,
            "final_decision": decision.chosen_proposal_id if decision else None,
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall conflict resolution statistics.

        Returns:
            Statistics dictionary
        """
        total = len(self._conflicts)
        resolved = len(self._decisions)

        return {
            "total_conflicts": total,
            "resolved": resolved,
            "unresolved": total - resolved,
            "resolution_rate": f"{(resolved / total * 100):.1f}%" if total > 0 else "0%",
            "active_conflicts": list(self._conflicts.keys()),
        }

    def invoke(
        self,
        tool_input: Union[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Invoke the tool for LangChain compatibility.

        Args:
            tool_input: Tool input as string or dict

        Returns:
            Tool output as dict
        """
        if isinstance(tool_input, str):
            return {"error": "Invalid input format. Expected dict with action and parameters."}

        action = tool_input.get("action")
        params = tool_input.get("params", {})

        if action == "detect":
            return self.detect_conflict(**params) or {"status": "no_conflict"}

        elif action == "resolve":
            return self.resolve_conflict(**params) or {"status": "resolution_failed"}

        elif action == "record_decision":
            return self.record_decision(**params)

        elif action == "details":
            conflict_id = params.get("conflict_id")
            return (
                self.get_conflict_details(conflict_id)
                if conflict_id
                else {"error": "Missing conflict_id"}
            )

        elif action == "statistics":
            return self.get_statistics()

        else:
            return {"error": f"Unknown action: {action}"}

    def clear(self) -> None:
        """Clear all tracked conflicts."""
        self._conflicts.clear()
        self._resolutions.clear()
        self._decisions.clear()
        self.detector.clear_conflicts()
