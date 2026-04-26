"""
Example 3: Project Goals Conflict Detection

Demonstrates detecting conflicts in project goals.
"""

from socratic_conflict import GoalsConflictChecker


def detect_goals_conflict():
    """
    Detect when conflicting project goals are proposed.
    """
    print("=" * 70)
    print("PROJECT GOALS CONFLICT DETECTION")
    print("=" * 70)
    print()

    checker = GoalsConflictChecker()

    print("Step 1: Existing Project Goals")
    print("-" * 70)

    class MockProject:
        tech_stack = []
        requirements = []
        goals = [
            "Achieve 99.99% uptime (SLA)",
            "Minimize operational costs",
            "Fast time-to-market"
        ]
        constraints = []

    project = MockProject()
    for goal in project.goals:
        print(f"  - {goal}")
    print()

    # Step 2: Propose conflicting goal
    print("Step 2: Propose New Goal")
    print("-" * 70)

    new_insights = {
        "goals": ["Maximize feature richness and redundancy"]
    }

    print(f"Proposed: {new_insights['goals'][0]}")
    print("(Proposer: Agent-FeatureDevelopment)")
    print()

    # Step 3: Check for conflicts
    print("Step 3: Goal Conflict Analysis")
    print("-" * 70)

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-FeatureDevelopment"
    )

    if conflict:
        print("CONFLICT DETECTED!")
        print(f"  Type: Goals")
        print(f"  Severity: {conflict.severity}")
        print(f"  Proposed: {conflict.new_value}")
        print(f"  May conflict with: {conflict.old_value}")
        print()
        print("Analysis:")
        print("  - High redundancy increases costs")
        print("  - May extend time-to-market")
        print("  - Could impact uptime SLA negatively")
        print()
        print("Suggestions:")
        for i, suggestion in enumerate(conflict.suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("No conflict detected")
    print()


if __name__ == "__main__":
    detect_goals_conflict()
    print("=" * 70)
