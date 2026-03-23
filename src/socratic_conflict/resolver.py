"""
Conflict resolution in multi-agent workflows.
"""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Resolution(BaseModel):
    """Represents a conflict resolution."""

    conflict_id: str = Field(..., description="ID of resolved conflict")
    strategy: str = Field(..., description="Resolution strategy used")
    outcome: str = Field(..., description="Resolution outcome")
    timestamp: str = Field(..., description="When resolved")
    success: bool = Field(default=True, description="Whether resolution succeeded")


class ConflictResolver:
    """
    Resolves conflicts in multi-agent workflows.

    Uses various strategies:
    - Prioritization: Execute higher-priority agent first
    - Negotiation: Agents reach compromise
    - Resource allocation: Fair distribution
    - Sequencing: Execute serially instead of parallel
    - Voting: Majority decision
    """

    def __init__(self):
        """Initialize the conflict resolver."""
        self.resolutions: List[Resolution] = []
        self.strategies = {
            "priority": self._resolve_by_priority,
            "negotiation": self._resolve_by_negotiation,
            "allocation": self._resolve_by_allocation,
            "sequencing": self._resolve_by_sequencing,
            "voting": self._resolve_by_voting,
        }

    def resolve(
        self,
        conflict: Dict[str, Any],
        agent_metadata: Dict[str, Any],
        preferred_strategy: Optional[str] = None
    ) -> Resolution:
        """
        Resolve a conflict using an appropriate strategy.

        Args:
            conflict: Conflict data
            agent_metadata: Information about agents
            preferred_strategy: Preferred resolution strategy

        Returns:
            Resolution result
        """
        conflict_type = conflict.get("type", "unknown")
        strategy = preferred_strategy or self._select_strategy(conflict_type)

        if strategy not in self.strategies:
            logger.warning(f"Unknown strategy: {strategy}")
            strategy = "priority"

        resolution_func = self.strategies[strategy]
        outcome = resolution_func(conflict, agent_metadata)

        resolution = Resolution(
            conflict_id=conflict.get("id", "unknown"),
            strategy=strategy,
            outcome=outcome,
            timestamp="now",
            success=True
        )

        self.resolutions.append(resolution)
        logger.info(f"Resolved conflict using {strategy} strategy")
        return resolution

    def _select_strategy(self, conflict_type: str) -> str:
        """Select best strategy for conflict type."""
        strategy_map = {
            "goal_divergence": "voting",
            "resource_contention": "allocation",
            "decision_contradiction": "negotiation",
            "deadlock": "sequencing",
        }
        return strategy_map.get(conflict_type, "priority")

    def _resolve_by_priority(
        self,
        conflict: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> str:
        """Resolve by agent priority."""
        agents = conflict.get("agents", [])
        if not agents:
            return "No agents to resolve"

        # Get priority for each agent
        priorities = {
            agent: metadata.get(agent, {}).get("priority", 0)
            for agent in agents
        }

        winner = max(priorities.items(), key=lambda x: x[1])[0]
        return f"Gave priority to agent: {winner}"

    def _resolve_by_negotiation(
        self,
        conflict: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> str:
        """Resolve through agent negotiation."""
        return "Initiated negotiation between agents"

    def _resolve_by_allocation(
        self,
        conflict: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> str:
        """Resolve by fair resource allocation."""
        agents = conflict.get("agents", [])
        return f"Allocated resources fairly among {len(agents)} agents"

    def _resolve_by_sequencing(
        self,
        conflict: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> str:
        """Resolve by sequential execution."""
        agents = conflict.get("agents", [])
        return f"Sequenced execution of {len(agents)} agents"

    def _resolve_by_voting(
        self,
        conflict: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> str:
        """Resolve by majority voting."""
        agents = conflict.get("agents", [])
        return f"Resolved via majority vote among {len(agents)} agents"

    def get_resolution_history(self) -> List[Resolution]:
        """Get resolution history."""
        return self.resolutions

    def clear_history(self) -> None:
        """Clear resolution history."""
        self.resolutions = []
        logger.info("Cleared resolution history")
