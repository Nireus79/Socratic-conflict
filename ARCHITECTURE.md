# socratic-conflict Architecture

Conflict detection and resolution system for multi-agent workflows.

## System Overview

socratic-conflict detects conflicts across multiple dimensions and provides resolution strategies. It uses a factory pattern with specialized checkers for different conflict types.

## Core Components

### 1. ConflictChecker Factory Pattern

Base class for conflict detection with specialized implementations:

- TechStackConflictChecker - Technology compatibility
- RequirementsConflictChecker - Requirement conflicts
- GoalsConflictChecker - Goal conflicts
- ConstraintsConflictChecker - Constraint violations

Each checker implements:
- `_extract_values()` - Extract from new insights
- `_get_existing_values()` - Get from project state
- `_find_conflict()` - Detect and analyze conflicts

### 2. Four Specialized Checkers

#### TechStackConflictChecker
Detects technology stack incompatibilities
- Checks for conflicting technologies
- Categorizes by conflict type (databases, languages, frameworks)
- Provides integration recommendations
- Severity: high for databases/languages, medium for others

#### RequirementsConflictChecker
Detects conflicting requirements using semantic analysis
- Identifies mutually exclusive requirements
- Checks for scope and performance conflicts
- Provides resolution suggestions
- Tracks requirement version history

#### GoalsConflictChecker
Detects conflicting project goals
- Identifies goal incompatibilities
- Checks for resource/timeline conflicts
- Suggests compromise goals
- Prioritizes based on strategic alignment

#### ConstraintsConflictChecker
Detects constraint violations and conflicts
- Budget constraint conflicts
- Timeline constraint conflicts
- Resource constraint conflicts
- Technical constraint conflicts

### 3. ConflictInfo Model

Represents a detected conflict:
- `conflict_id` - Unique identifier
- `conflict_type` - tech_stack, requirements, goals, or constraints
- `old_value` - Original value causing conflict
- `new_value` - New value causing conflict
- `old_author` - Who set the original value
- `new_author` - Who proposed the new value
- `old_timestamp` - When original value was set
- `new_timestamp` - When new value was proposed
- `severity` - low, medium, or high
- `suggestions` - List of resolution suggestions

### 4. Rules Engine

Maps conflict pairs to categories:
- databases - Conflicting database combinations
- languages - Conflicting language combinations
- frameworks - Conflicting framework combinations
- requirements - Conflicting requirement patterns

Function: `find_conflict_category(value1, value2) -> str or None`

## Detection Pipeline

```
New Insight/Change
    |
    v
Appropriate Checker Selected
    |
    v
Extract New Values
    |
    v
Get Existing Values from Project
    |
    v
Run Conflict Rules
    |
    v
Analyze Severity
    |
    v
Generate Suggestions
    |
    v
Return ConflictInfo (if conflict found)
```

## Resolution Strategies

The system supports resolution through:

### 1. Voting Strategy
- Each stakeholder votes on alternatives
- Simple majority or weighted voting
- Tracks vote history

### 2. Consensus Strategy
- All stakeholders must agree
- May take longer but ensures buy-in
- Requires compromise solutions

### 3. Weighted Priority Strategy
- Stakeholders have different weights
- High-priority stakeholder's preference wins
- Useful for hierarchical organizations

### 4. Priority-Based Strategy
- Automatic resolution based on priority rules
- Highest priority suggestion wins
- Transparent decision criteria

### 5. Hybrid Strategy
- Combines multiple strategies
- Escalates to human review if needed
- Learns from past resolutions

## Severity Calculation

Conflicts are rated: low, medium, high

### Low Severity
- Non-critical conflicts
- Easy workarounds available
- Minor impact on project

### Medium Severity
- Important conflicts
- Moderate impact on project
- Requires thoughtful resolution

### High Severity
- Critical conflicts
- Major project impact
- Requires escalation/decision

## History Tracking

Maintains conflict history with:
- Conflict record timestamp
- Resolution history
- Previous stakeholder positions
- Outcome tracking for learning

## Integration Points

### With socratic-nexus (LLM Client)
- Use LLMs to analyze conflict text
- Generate better resolution suggestions
- Improve conflict categorization

### With socratic-analyzer (Code Analysis)
- Detect conflicts in code structure
- Analyze design conflicts
- Identify architecture conflicts

### With socratic-agents (Agent Framework)
- Agents propose changes
- Conflict detection prevents invalid states
- Resolution strategies guide decision-making

### With socratic-workflow (Task Management)
- Detect workflow conflicts
- Block conflicting task assignments
- Suggest resolution workflows

## Consensus Algorithms

When multiple conflicts exist:

### 1. Majority Rules
- Count stakeholder preferences
- Simple majority wins
- Democratic approach

### 2. Consensus Seeking
- Find common ground
- Iterative refinement
- All stakeholders agree

### 3. Weighted Consensus
- Stakeholder weights matter
- Weighted majority needed
- Respects hierarchy

### 4. Pareto Optimization
- Find solution benefiting most
- Minimize harm to others
- Compromise-oriented

### 5. Escalation
- Conflicts auto-escalate if unresolved
- Human review required
- Documented decision path

## Performance Characteristics

- Detection: O(n*m) where n = new values, m = existing values
- Rule Matching: O(r) where r = number of conflict rules
- Severity Analysis: O(1) - lookup based category
- Memory: O(conflicts) for history tracking

---

Part of the Socratic Ecosystem | Factory Pattern | Pure Detection System
