# Socratic Conflict - FAQ by Scenario

## Detecting Conflicts

How do I detect data conflicts?

```python
from socratic_conflict import ConflictDetector, Proposal

detector = ConflictDetector()
conflict = detector.detect_data_conflict(
    field_name="priority",
    values={"agent1": "high", "agent2": "low"},
    agents=["agent1", "agent2"]
)
```

## Resolving with Voting

How do I use voting?

```python
from socratic_conflict import VotingStrategy

strategy = VotingStrategy()
resolution = strategy.resolve(conflict)
print(f"Winner: {resolution.recommended_proposal_id}")
print(f"Confidence: {resolution.confidence:.2%}")
```

## Using Consensus

How do I require consensus?

```python
from socratic_conflict.consensus import SupermajorityConsensus

algorithm = SupermajorityConsensus(threshold=0.75)
proposal_id, confidence = algorithm.reach_consensus(conflict)
```

## Tracking History

How do I track decisions?

```python
from socratic_conflict.history import HistoryTracker

tracker = HistoryTracker()
tracker.add_conflict(conflict)
tracker.add_resolution(resolution)

history = tracker.get_conflict_history(conflict.conflict_id)
stats = tracker.get_statistics()
```

## Custom Strategies

How do I create custom resolution?

```python
class CustomStrategy:
    def resolve(self, conflict):
        # Custom logic
        return resolution
```
