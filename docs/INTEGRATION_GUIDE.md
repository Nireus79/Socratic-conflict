# Socratic Conflict - Integration Guide

## Socratic Agents Integration

Detect/resolve conflicts between agent proposals:

```python
from socratic_conflict import ConflictDetector
from socratic_agents import AgentOrchestrator

detector = ConflictDetector()
orchestrator = AgentOrchestrator(llm_client=llm)

# If agents disagree, detect and resolve conflict
```

## Socratic Workflow Integration

Handle conflicting execution paths:

```python
from socratic_conflict import ConflictDetector
from socratic_workflow import Workflow

detector = ConflictDetector()
# Detect workflow conflicts during execution
```

## Custom Integration

Use in any multi-agent system:

```python
from socratic_conflict import ConflictDetector, VotingStrategy

detector = ConflictDetector()
strategy = VotingStrategy()

# In your agent coordination logic
conflict = detector.detect_decision_conflict(proposals, agents)
resolution = strategy.resolve(conflict)
```
