from __future__ import annotations

"""Conflict detection and resolution for Socrates AI"""

from .base import ConflictChecker
from .checkers import (
    ConstraintsConflictChecker,
    GoalsConflictChecker,
    RequirementsConflictChecker,
    TechStackConflictChecker,
)
from .models import ConflictInfo, ProjectContext
from .rules import CONFLICT_RULES, find_conflict_category

__all__ = [
    "ConflictChecker",
    "TechStackConflictChecker",
    "RequirementsConflictChecker",
    "GoalsConflictChecker",
    "ConstraintsConflictChecker",
    "ConflictInfo",
    "ProjectContext",
    "CONFLICT_RULES",
    "find_conflict_category",
]
