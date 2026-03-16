# Socratic Conflict - Architecture

## System Overview

Socratic Conflict detects conflicts between agents and resolves them using multiple strategies and consensus algorithms.

## Core Components

### 1. ConflictDetector
Automatically detects conflicts.

Conflict types:
- Data conflicts (disagreement on values)
- Decision conflicts (different proposals)
- Workflow conflicts (conflicting execution paths)

### 2. Resolution Strategies (5)
1. VotingStrategy - Simple majority
2. ConsensusStrategy - Highest confidence
3. WeightedStrategy - Agent weight × confidence
4. PriorityStrategy - Priority rules
5. HybridStrategy - Multiple strategies

### 3. Consensus Algorithms (5)
1. MajorityConsensus - >50%
2. UnanimousConsensus - 100%
3. SupermajorityConsensus - Configurable
4. RankedChoiceConsensus - Confidence-based
5. QuorumConsensus - Quorum + majority

### 4. History Tracker
Tracks all conflicts and resolutions.

Features:
- Full conflict history
- Decision versioning
- Statistics and analytics
