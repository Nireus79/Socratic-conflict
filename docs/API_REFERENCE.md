# Socratic Conflict - API Reference

## ConflictDetector

Methods:
- `detect_data_conflict(field_name, values, agents)` - Detect data conflict
- `detect_decision_conflict(proposals, agents)` - Detect decision conflict
- `detect_workflow_conflict(workflow_id, conflicting_steps)` - Detect workflow conflict
- `calculate_severity(conflict)` - Calculate severity

## Resolution Strategies

### VotingStrategy
```python
strategy = VotingStrategy()
resolution = strategy.resolve(conflict)
```

### ConsensusStrategy
Selects highest confidence proposal.

### WeightedStrategy
```python
strategy = WeightedStrategy(weights={
    "expert_agent": 0.9,
    "junior_agent": 0.3
})
```

### PriorityStrategy
```python
strategy = PriorityStrategy(priority_rules={
    "admin": 10,
    "manager": 5,
    "user": 1
})
```

### HybridStrategy
Combines multiple strategies.

## Consensus Algorithms

- MajorityConsensus - >50%
- UnanimousConsensus - 100%
- SupermajorityConsensus(threshold)
- RankedChoiceConsensus
- QuorumConsensus(quorum_fraction)

## HistoryTracker

- `add_conflict(conflict)` - Log conflict
- `add_resolution(resolution)` - Log resolution
- `get_conflict_history(conflict_id)` - Get history
- `get_statistics()` - Get statistics
