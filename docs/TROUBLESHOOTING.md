# Socratic Conflict - Troubleshooting

## Detection Issues

### No conflicts detected

Cause: Agent disagreements subtle

Solution: Use appropriate detection threshold

## Resolution Issues

### No consensus reached

Cause: Unanimous algorithm with disagreement

Solution: Use MajorityConsensus instead:
```python
from socratic_conflict.consensus import MajorityConsensus
algorithm = MajorityConsensus()
```

### Unexpected resolution

Cause: Strategy weights incorrect

Solution: Review strategy configuration

## Performance Issues

### Slow resolution

Cause: Complex conflict graph

Solution: Simplify agent proposals

## Integration Issues

### Conflicts not tracked

Cause: History tracker not initialized

Solution: Initialize tracker:
```python
from socratic_conflict.history import HistoryTracker
tracker = HistoryTracker()
```
