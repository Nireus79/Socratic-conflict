"""
Example 2: Requirements Conflict Detection

Demonstrates detecting conflicts in project requirements.
"""

from socratic_conflict import RequirementsConflictChecker


def detect_requirements_conflict():
    """
    Detect when conflicting requirements are proposed.
    """
    print("=" * 70)
    print("REQUIREMENTS CONFLICT DETECTION")
    print("=" * 70)
    print()

    checker = RequirementsConflictChecker()

    print("Step 1: Existing Requirements")
    print("-" * 70)

    class MockProject:
        tech_stack = []
        requirements = [
            "Real-time data processing",
            "Batch processing pipeline",
            "REST API interface"
        ]
        goals = []
        constraints = []

    project = MockProject()
    for req in project.requirements:
        print(f"  - {req}")
    print()

    # Step 2: Propose conflicting requirement
    print("Step 2: Propose New Requirement")
    print("-" * 70)

    new_insights = {
        "requirements": ["Minimalist synchronous processing"]
    }

    print(f"Proposed: {new_insights['requirements'][0]}")
    print("(Proposer: Agent-PerformanceOptimizer)")
    print()

    # Step 3: Check for conflicts
    print("Step 3: Semantic Conflict Analysis")
    print("-" * 70)

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-PerformanceOptimizer"
    )

    if conflict:
        print("CONFLICT DETECTED!")
        print(f"  Type: Requirements")
        print(f"  Severity: {conflict.severity}")
        print(f"  Conflicts with: {conflict.old_value}")
        print()
        print("Suggestions for resolution:")
        for i, suggestion in enumerate(conflict.suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("No conflict detected")
    print()


def non_conflicting_requirement():
    """
    Example of adding non-conflicting requirement.
    """
    print("=" * 70)
    print("NON-CONFLICTING REQUIREMENT")
    print("=" * 70)
    print()

    checker = RequirementsConflictChecker()

    class MockProject:
        tech_stack = []
        requirements = [
            "Mobile-friendly UI",
            "Cross-platform support"
        ]
        goals = []
        constraints = []

    project = MockProject()
    print(f"Current requirements:")
    for req in project.requirements:
        print(f"  - {req}")
    print()

    new_insights = {
        "requirements": ["Accessibility compliance (WCAG 2.1)"]
    }

    print(f"Proposed: {new_insights['requirements'][0]}")
    print()

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-AccessibilityLead"
    )

    if not conflict:
        print("[OK] No conflict - requirement can be added")
    print()


if __name__ == "__main__":
    detect_requirements_conflict()
    print()
    non_conflicting_requirement()
    print("=" * 70)
