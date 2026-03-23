"""
Socratic Conflict - Multi-agent workflow conflict detection and resolution

Provides tools for detecting and resolving conflicts in multi-agent systems.
"""

__version__ = "0.1.0"

from .detector import ConflictDetector
from .resolver import ConflictResolver

__all__ = [
    "ConflictDetector",
    "ConflictResolver",
]
