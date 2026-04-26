"""
Example 4: Constraints Conflict Detection

Demonstrates detecting conflicts in project constraints.
"""

from socratic_conflict import ConstraintsConflictChecker


def detect_budget_constraint_conflict():
    """
    Detect budget constraint violations.
    """
    print("=" * 70)
    print("BUDGET CONSTRAINT CONFLICT")
    print("=" * 70)
    print()

    checker = ConstraintsConflictChecker()

    print("Step 1: Existing Constraints")
    print("-" * 70)

    class MockProject:
        tech_stack = []
        requirements = []
        goals = []
        constraints = [
            "Budget: $500,000",
            "Timeline: 6 months",
            "Team size: max 10 engineers"
        ]

    project = MockProject()
    for constraint in project.constraints:
        print(f"  - {constraint}")
    print()

    # Step 2: Propose conflicting constraint
    print("Step 2: Propose Additional Constraint")
    print("-" * 70)

    new_insights = {
        "constraints": ["Hire 15 specialized contractors"]
    }

    print(f"Proposed: {new_insights['constraints'][0]}")
    print("(Proposer: Agent-TeamPlanning)")
    print()

    # Step 3: Check for conflicts
    print("Step 3: Constraint Conflict Analysis")
    print("-" * 70)

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-TeamPlanning"
    )

    if conflict:
        print("CONFLICT DETECTED!")
        print(f"  Type: Constraints")
        print(f"  Severity: {conflict.severity}")
        print(f"  Violates: {conflict.old_value}")
        print(f"  Proposed: {conflict.new_value}")
        print()
        print("Impact Analysis:")
        print("  - Exceeds team size constraint (15 > 10)")
        print("  - May exceed budget with contractor costs")
        print("  - Communication overhead increases")
        print()
        print("Suggestions:")
        for i, suggestion in enumerate(conflict.suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("No conflict detected")
    print()


def timeline_constraint_conflict():
    """
    Detect timeline constraint violations.
    """
    print("=" * 70)
    print("TIMELINE CONSTRAINT CONFLICT")
    print("=" * 70)
    print()

    checker = ConstraintsConflictChecker()

    class MockProject:
        tech_stack = []
        requirements = []
        goals = []
        constraints = [
            "Timeline: 6 months",
            "MVP delivery: 3 months"
        ]

    project = MockProject()
    print(f"Current constraints:")
    for constraint in project.constraints:
        print(f"  - {constraint}")
    print()

    new_insights = {
        "constraints": ["Full feature set completion: 2 months"]
    }

    print(f"Proposed: {new_insights['constraints'][0]}")
    print()

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-ProjectManager"
    )

    if conflict:
        print("CONFLICT DETECTED!")
        print(f"  Severity: {conflict.severity}")
        print(f"  Timeline conflict detected")
        print("  Cannot complete full features in 2 months")
        print("  when MVP needs 3 months")
    print()


if __name__ == "__main__":
    detect_budget_constraint_conflict()
    print()
    timeline_constraint_conflict()
    print("=" * 70)
