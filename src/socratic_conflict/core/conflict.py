"""Core conflict models and data structures."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Proposal:
    """A proposal or decision option in a conflict."""

    proposal_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    source_agent: str = ""  # Which agent proposed this
    proposed_at: datetime = field(default_factory=datetime.utcnow)
    rationale: str = ""
    expected_outcome: str = ""
    confidence: float = 0.0  # 0.0-1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "source_agent": self.source_agent,
            "proposed_at": self.proposed_at.isoformat(),
            "rationale": self.rationale,
            "expected_outcome": self.expected_outcome,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Proposal":
        """Deserialize from dictionary."""
        data = data.copy()
        data["proposed_at"] = datetime.fromisoformat(data["proposed_at"])
        return cls(**data)


@dataclass
class Conflict:
    """Represents a conflict or disagreement between agents/proposals."""

    conflict_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    conflict_type: str = ""  # "data", "decision", "workflow", "consensus"
    severity: str = "medium"  # low, medium, high, critical
    related_agents: List[str] = field(default_factory=list)
    proposals: List[Proposal] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "conflict_id": self.conflict_id,
            "title": self.title,
            "description": self.description,
            "conflict_type": self.conflict_type,
            "severity": self.severity,
            "related_agents": self.related_agents,
            "proposals": [p.to_dict() for p in self.proposals],
            "detected_at": self.detected_at.isoformat(),
            "context": self.context,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conflict":
        """Deserialize from dictionary."""
        data = data.copy()
        data["detected_at"] = datetime.fromisoformat(data["detected_at"])
        data["proposals"] = [Proposal.from_dict(p) for p in data["proposals"]]
        return cls(**data)


@dataclass
class Resolution:
    """A proposed resolution to a conflict."""

    resolution_id: str = field(default_factory=lambda: str(uuid4()))
    conflict_id: str = ""
    strategy: str = ""  # "voting", "consensus", "weighted", "priority", "hybrid"
    recommended_proposal_id: Optional[str] = None
    confidence: float = 0.0  # 0.0-1.0 confidence in this resolution
    rationale: str = ""
    expected_outcome: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    votes: Dict[str, str] = field(default_factory=dict)  # agent -> proposal_id
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "resolution_id": self.resolution_id,
            "conflict_id": self.conflict_id,
            "strategy": self.strategy,
            "recommended_proposal_id": self.recommended_proposal_id,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "expected_outcome": self.expected_outcome,
            "created_at": self.created_at.isoformat(),
            "votes": self.votes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Resolution":
        """Deserialize from dictionary."""
        data = data.copy()
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class ConflictDecision:
    """A final decision made to resolve a conflict."""

    decision_id: str = field(default_factory=lambda: str(uuid4()))
    conflict_id: str = ""
    resolution_id: str = ""
    chosen_proposal_id: str = ""
    decided_at: datetime = field(default_factory=datetime.utcnow)
    decided_by: str = ""  # Who made the final decision (agent, system, user)
    rationale: str = ""
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "decision_id": self.decision_id,
            "conflict_id": self.conflict_id,
            "resolution_id": self.resolution_id,
            "chosen_proposal_id": self.chosen_proposal_id,
            "decided_at": self.decided_at.isoformat(),
            "decided_by": self.decided_by,
            "rationale": self.rationale,
            "version": self.version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConflictDecision":
        """Deserialize from dictionary."""
        data = data.copy()
        data["decided_at"] = datetime.fromisoformat(data["decided_at"])
        return cls(**data)
