"""
Conflict detection in multi-agent workflows.
"""

import logging
from typing import Any, Dict, List

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Conflict(BaseModel):
    """Represents a detected conflict."""

    id: str = Field(..., description="Conflict ID")
    agents: List[str] = Field(..., description="Agents involved in conflict")
    type: str = Field(..., description="Type of conflict")
    severity: str = Field(default="medium", description="Severity level")
    description: str = Field(..., description="Conflict description")
    timestamp: str = Field(..., description="When conflict was detected")
    resolved: bool = Field(default=False, description="Whether conflict is resolved")


class ConflictDetector:
    """
    Detects conflicts in multi-agent workflows.

    Monitors agent interactions and identifies conflicts such as:
    - Diverging goals
    - Resource contention
    - Contradictory decisions
    - Deadlocks
    """

    def __init__(self):
        """Initialize the conflict detector."""
        self.conflicts: List[Conflict] = []
        self.detection_rules = self._init_detection_rules()

    def _init_detection_rules(self) -> Dict[str, Any]:
        """Initialize conflict detection rules."""
        return {
            "goal_divergence": self._detect_goal_divergence,
            "resource_contention": self._detect_resource_contention,
            "decision_contradiction": self._detect_decision_contradiction,
            "deadlock": self._detect_deadlock,
        }

    def detect_conflicts(self, agent_states: Dict[str, Any]) -> List[Conflict]:
        """
        Detect conflicts from agent states.

        Args:
            agent_states: Dictionary mapping agent IDs to their states

        Returns:
            List of detected conflicts
        """
        detected = []

        # Apply each detection rule
        for rule_name, rule_func in self.detection_rules.items():
            conflicts = rule_func(agent_states)
            detected.extend(conflicts)

        self.conflicts.extend(detected)
        logger.info(f"Detected {len(detected)} conflicts")
        return detected

    def _detect_goal_divergence(self, agent_states: Dict[str, Any]) -> List[Conflict]:
        """Detect conflicts from diverging agent goals."""
        conflicts = []

        agent_ids = list(agent_states.keys())
        for i, agent_a in enumerate(agent_ids):
            for agent_b in agent_ids[i+1:]:
                goal_a = agent_states[agent_a].get("goal", "")
                goal_b = agent_states[agent_b].get("goal", "")

                # Simple heuristic: if goals have minimal overlap, flag conflict
                if goal_a and goal_b and goal_a.lower() != goal_b.lower():
                    conflicts.append(Conflict(
                        id=f"conflict_{len(conflicts)}",
                        agents=[agent_a, agent_b],
                        type="goal_divergence",
                        severity="high",
                        description=f"Agents have diverging goals: '{goal_a}' vs '{goal_b}'",
                        timestamp="now"
                    ))

        return conflicts

    def _detect_resource_contention(self, agent_states: Dict[str, Any]) -> List[Conflict]:
        """Detect conflicts from resource contention."""
        conflicts = []

        resources = {}
        for agent_id, state in agent_states.items():
            for resource in state.get("resources", []):
                if resource not in resources:
                    resources[resource] = []
                resources[resource].append(agent_id)

        # Flag resources claimed by multiple agents
        for resource, agents in resources.items():
            if len(agents) > 1:
                conflicts.append(Conflict(
                    id=f"conflict_{len(conflicts)}",
                    agents=agents,
                    type="resource_contention",
                    severity="medium",
                    description=f"Multiple agents competing for resource: {resource}",
                    timestamp="now"
                ))

        return conflicts

    def _detect_decision_contradiction(self, agent_states: Dict[str, Any]) -> List[Conflict]:
        """Detect conflicts from contradictory decisions."""
        return []  # Implementation depends on decision tracking

    def _detect_deadlock(self, agent_states: Dict[str, Any]) -> List[Conflict]:
        """Detect circular wait deadlocks."""
        return []  # Implementation depends on dependency tracking

    def get_conflicts(self, agent_id: str = None) -> List[Conflict]:
        """
        Get detected conflicts.

        Args:
            agent_id: Optional agent ID to filter conflicts

        Returns:
            List of conflicts
        """
        if agent_id:
            return [c for c in self.conflicts if agent_id in c.agents]
        return self.conflicts

    def clear_conflicts(self) -> None:
        """Clear conflict history."""
        self.conflicts = []
        logger.info("Cleared conflict history")
