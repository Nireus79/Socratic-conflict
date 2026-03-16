"""Framework integrations for Socratic Conflict."""

from socratic_conflict.integrations.langchain import ConflictResolutionTool
from socratic_conflict.integrations.openclaw import SocraticConflictSkill

__all__ = ["SocraticConflictSkill", "ConflictResolutionTool"]
