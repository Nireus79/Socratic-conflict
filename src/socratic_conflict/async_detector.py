"""Async wrapper for ConflictDetector - enables non-blocking conflict detection and resolution."""

import asyncio
from typing import Any, Dict, List, Optional

from socratic_conflict.core.conflict import Conflict, Resolution
from socratic_conflict.detection.detector import ConflictDetector
from socratic_conflict.resolution.strategies import ResolutionStrategy


class AsyncConflictDetector:
    """
    Asynchronous wrapper for ConflictDetector.

    Provides non-blocking async operations for conflict detection and resolution
    using asyncio.to_thread() pattern for CPU-bound operations.

    Usage:
        detector = AsyncConflictDetector()
        conflict = await detector.detect_data_conflict("field", values, agents)
        resolution = await detector.resolve(conflict, strategy)
    """

    def __init__(self):
        """Initialize AsyncConflictDetector."""
        self._detector = ConflictDetector()

    # ==================== Detection operations ====================

    async def detect_data_conflict(
        self,
        field_name: str,
        values: Dict[str, Any],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in data values asynchronously.

        Args:
            field_name: Name of the field with conflicting values
            values: Dict mapping agent_name to their proposed value
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.detect_data_conflict,
            field_name,
            values,
            agents,
            context,
        )

    async def detect_decision_conflict(
        self,
        decision_name: str,
        proposals: Dict[str, str],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in decision-making asynchronously.

        Args:
            decision_name: Name of the decision
            proposals: Dict mapping agent_name to their proposal/rationale
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.detect_decision_conflict,
            decision_name,
            proposals,
            agents,
            context,
        )

    async def detect_workflow_conflict(
        self,
        workflow_name: str,
        task_results: Dict[str, Dict[str, Any]],
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts in workflow execution asynchronously.

        Args:
            workflow_name: Name of the workflow
            task_results: Dict mapping agent_name to their task results
            agents: List of agent names
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.detect_workflow_conflict,
            workflow_name,
            task_results,
            agents,
            context,
        )

    async def detect_consensus_conflict(
        self,
        topic: str,
        votes: Dict[str, str],
        agents: List[str],
        required_consensus: float = 0.8,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Conflict]:
        """Detect conflicts when consensus cannot be reached asynchronously.

        Args:
            topic: Topic being voted on
            votes: Dict mapping agent_name to their vote
            agents: List of agent names
            required_consensus: Consensus threshold required (0.0-1.0)
            context: Additional context about the conflict

        Returns:
            Conflict object if conflict detected, None otherwise
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.detect_consensus_conflict,
            topic,
            votes,
            agents,
            required_consensus,
            context,
        )

    # ==================== Resolution operations ====================

    async def resolve(
        self,
        conflict: Conflict,
        strategy: ResolutionStrategy,
    ) -> Optional[Resolution]:
        """Resolve a conflict asynchronously.

        Args:
            conflict: Conflict to resolve
            strategy: Resolution strategy to use

        Returns:
            Resolution object or None if unable to resolve
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            strategy.resolve,
            conflict,
        )

    async def resolve_multiple(
        self,
        conflicts: List[Conflict],
        strategy: ResolutionStrategy,
    ) -> List[Optional[Resolution]]:
        """Resolve multiple conflicts asynchronously.

        Args:
            conflicts: List of conflicts to resolve
            strategy: Resolution strategy to use

        Returns:
            List of Resolution objects or None for unresolvable conflicts
        """
        tasks = [self.resolve(conflict, strategy) for conflict in conflicts]
        return await asyncio.gather(*tasks)

    # ==================== Query operations ====================

    async def get_detected_conflicts(self) -> List[Conflict]:
        """Get all detected conflicts asynchronously.

        Returns:
            List of all detected conflicts
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._detector.detected_conflicts,
        )

    async def get_conflicts_by_type(
        self,
        conflict_type: str,
    ) -> List[Conflict]:
        """Get conflicts by type asynchronously.

        Args:
            conflict_type: Type of conflict to filter by

        Returns:
            List of conflicts matching the type
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.get_conflicts_by_type,
            conflict_type,
        )

    async def get_conflicts_by_severity(
        self,
        severity: str,
    ) -> List[Conflict]:
        """Get conflicts by severity asynchronously.

        Args:
            severity: Severity level to filter by (low, medium, high, critical)

        Returns:
            List of conflicts matching the severity
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.get_conflicts_by_severity,
            severity,
        )

    async def get_agent_conflicts(
        self,
        agent_name: str,
    ) -> List[Conflict]:
        """Get conflicts involving a specific agent asynchronously.

        Args:
            agent_name: Name of the agent

        Returns:
            List of conflicts involving the agent
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._detector.get_agent_conflicts,
            agent_name,
        )

    async def clear_conflicts(self) -> None:
        """Clear all detected conflicts asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._detector.detected_conflicts.clear(),
        )
