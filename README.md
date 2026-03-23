# Socratic Conflict

Multi-agent workflow conflict detection and resolution for the Socratic AI platform.

## Features

- **Automatic Detection**: Identifies conflicts in multi-agent systems
- **Multiple Strategies**: Priority-based, negotiation, voting, resource allocation, sequencing
- **Severity Tracking**: Categorizes conflicts by severity
- **Resolution History**: Maintains audit trail of resolutions
- **Agent Metadata Support**: Uses agent metadata for smarter resolution

## Installation

```bash
pip install socratic-conflict
```

With agents support:

```bash
pip install socratic-conflict[agents]
```

## Quick Start

```python
from socratic_conflict import ConflictDetector, ConflictResolver

# Detect conflicts
detector = ConflictDetector()
agent_states = {
    "agent_a": {"goal": "finish task 1", "resources": ["database"]},
    "agent_b": {"goal": "finish task 2", "resources": ["database"]},
}

conflicts = detector.detect_conflicts(agent_states)

# Resolve conflicts
resolver = ConflictResolver()
for conflict in conflicts:
    resolution = resolver.resolve(conflict, {})
    print(resolution.outcome)
```

## Components

### ConflictDetector

Detects conflicts from agent states.

```python
detector = ConflictDetector()
conflicts = detector.detect_conflicts(agent_states)
```

Detects:
- Goal divergence
- Resource contention
- Decision contradictions
- Deadlocks

### ConflictResolver

Resolves detected conflicts using various strategies.

```python
resolver = ConflictResolver()
resolution = resolver.resolve(conflict, agent_metadata, preferred_strategy="voting")
```

Strategies:
- **priority**: Higher-priority agent proceeds
- **voting**: Majority vote decides
- **negotiation**: Agents reach compromise
- **allocation**: Fair resource distribution
- **sequencing**: Sequential instead of parallel execution

## License

MIT
