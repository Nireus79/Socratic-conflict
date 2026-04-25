"""
Data models for Socratic Conflict

Extracted from Socrates v1.3.3
"""

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ConflictInfo:
    """Represents a conflict detected in project specifications"""

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


@dataclass
class ProjectContext:
    """Represents a project's complete context and metadata"""

    project_id: str
    name: str
    owner: str
    phase: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    collaborators: List[str] = field(
        default=None
    )  # DEPRECATED: Kept for backward compatibility. Use team_members instead.
    description: str = ""
    goals: str = ""
    requirements: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    team_structure: str = "individual"
    language_preferences: str = "python"
    deployment_target: str = "local"
    code_style: str = "standard"
    conversation_history: List[Dict] = field(default_factory=list)
    chat_mode: str = "socratic"  # "socratic" or "direct" mode
    is_archived: bool = False
    archived_at: Optional[datetime.datetime] = None
    progress: int = 0  # 0-100 percentage
    status: str = "active"  # active, completed, on-hold
    project_type: str = (
        "software"  # Type of project (software, business, creative, research, marketing, educational)
    )

    # System project tracking (for onboarding and special projects)
    is_system_project: bool = False  # Not counted in subscription quotas
    system_project_type: Optional[str] = None  # "onboarding", "sandbox", etc.

    # Team management (NEW)
    team_members: Optional[List[Any]] = (
        None  # Team members with roles (supersedes collaborators)
    )
    pending_questions: Optional[List[Dict]] = None  # Question queue for team projects

    # Notes tracking
    notes: Optional[List[Dict]] = None  # Project notes list

    # Code history tracking
    code_history: Optional[List[Dict]] = None  # History of generated code with metadata

    # Maturity tracking fields
    phase_maturity_scores: Optional[Dict[str, float]] = None  # Per-phase maturity (0-100)
    overall_maturity: float = 0.0  # Overall project maturity (0-100)
    category_scores: Optional[Dict[str, Dict[str, float]]] = (
        None  # Category scores by phase
    )
    categorized_specs: Optional[Dict[str, List[Dict[str, Any]]]] = (
        None  # Specs organized by phase and category
    )
    maturity_history: Optional[List[Dict[str, Any]]] = None  # Historical maturity events

    # Analytics tracking fields (real-time metrics updated after each Q&A)
    analytics_metrics: Optional[Dict[str, Any]] = None  # Real-time analytics metrics

    # Workflow optimization fields (NEW)
    workflow_definitions: Optional[Dict[str, Any]] = (
        None  # Workflow definitions by phase
    )
    workflow_approval_requests: Optional[List[Dict[str, Any]]] = (
        None  # History of approval requests
    )
    active_workflow_execution: Optional[Dict[str, Any]] = (
        None  # Current workflow execution state
    )
    workflow_history: Optional[List[Dict[str, Any]]] = (
        None  # Completed workflows with metrics
    )
    metadata: Optional[Dict[str, Any]] = (
        None  # Project metadata (use_workflow_optimization flag, etc.)
    )

    # LLM Provider configuration
    llm_configuration: Optional[Dict[str, Any]] = (
        None  # LLM provider config (provider, model, temperature, etc.)
    )

    # GitHub repository tracking (for imported projects)
    repository_url: Optional[str] = None  # GitHub repository URL
    repository_owner: Optional[str] = None  # Repository owner username
    repository_name: Optional[str] = None  # Repository name
    repository_description: Optional[str] = None  # Repository description
    repository_language: Optional[str] = None  # Primary programming language
    repository_imported_at: Optional[datetime.datetime] = None  # When repo was imported
    repository_file_count: int = 0  # Number of files in repository
    repository_has_tests: bool = False  # Whether repository has tests

    # Export & GitHub Publishing Tracking (NEW)
    last_export_time: Optional[datetime.datetime] = None  # When project was last exported
    last_export_format: Optional[str] = None  # Last export format used (zip, tar, tar.gz, tar.bz2)
    export_count: int = 0  # Total number of exports

    # GitHub Publishing Status (NEW)
    is_published_to_github: bool = False  # Whether project has been published to GitHub
    github_repo_url: Optional[str] = None  # URL of GitHub repository created from this project
    github_clone_url: Optional[str] = None  # Git clone URL (https or ssh)
    github_published_date: Optional[datetime.datetime] = None  # When published to GitHub
    github_repo_private: bool = True  # Whether GitHub repo is private
    github_username: Optional[str] = None  # GitHub username that owns the published repo

    # Git Repository Status (NEW)
    has_git_initialized: bool = False  # Whether git repo has been initialized locally
    git_branch: Optional[str] = None  # Current git branch name
    git_remote_url: Optional[str] = None  # Git remote URL
    uncommitted_changes: bool = False  # Whether there are uncommitted changes
