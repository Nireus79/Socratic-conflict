"""
Data models for Socratic Conflict

Extracted from Socrates v1.3.3
"""

from dataclasses import dataclass, asdict
from typing import List


@dataclass
class ConflictInfo:
    @staticmethod
    def from_dict(data: dict) -> "ConflictInfo":
        """Deserialize from dictionary."""
        return ConflictInfo(**data)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        from dataclasses import asdict

        return asdict(self)

    conflict_id: str
    conflict_type: str  # 'tech_stack', 'requirements', 'goals', 'constraints'
    old_value: str
    new_value: str
    old_author: str
    new_author: str
    old_timestamp: str
    new_timestamp: str
    severity: str  # 'low', 'medium', 'high'
    suggestions: List[str]

    @staticmethod
    def from_dict(data: dict) -> "ConflictInfo":
        """Deserialize from dictionary."""
        return ConflictInfo(**data)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        from dataclasses import asdict

        return asdict(self)
