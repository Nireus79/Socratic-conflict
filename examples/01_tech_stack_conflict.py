"""
Example 1: Technology Stack Conflict Detection

Demonstrates detecting conflicts when new technologies are proposed
for existing projects.
"""

from socratic_conflict import TechStackConflictChecker, ConflictInfo


def detect_tech_stack_conflict():
    """
    Detect when incompatible technologies are proposed.
    """
    print("=" * 70)
    print("TECHNOLOGY STACK CONFLICT DETECTION")
    print("=" * 70)
    print()

    # Initialize the tech stack conflict checker
    checker = TechStackConflictChecker()

    print("Step 1: Existing Project Tech Stack")
    print("-" * 70)

    # Simulate a project context
    class MockProject:
        tech_stack = ["Python", "PostgreSQL", "React", "Docker"]
        requirements = []
        goals = []
        constraints = []

    project = MockProject()
    print(f"Current tech stack: {project.tech_stack}")
    print()

    # Step 2: Propose new technology
    print("Step 2: Propose New Technology")
    print("-" * 70)

    new_insights = {
        "tech_stack": ["MongoDB"]  # NoSQL database proposed
    }

    print(f"Proposed technology: {new_insights['tech_stack']}")
    print("(Proposer: Agent-DataEngineer)")
    print()

    # Step 3: Check for conflicts
    print("Step 3: Conflict Detection Analysis")
    print("-" * 70)

    conflict = checker.check(
        insights=new_insights,
        project=project,
        current_user="Agent-DataEngineer"
    )

    if conflict:
        print(f"CONFLICT DETECTED!")
        print(f"  Type: {conflict.conflict_type}")
        print(f"  Severity: {conflict.severity}")
        print(f"  Existing: {conflict.old_value}")
        print(f"  Proposed: {conflict.new_value}")
        print(f"  Proposer: {conflict.new_author}")
        print()
        print(f"Suggestions:")
        for i, suggestion in enumerate(conflict.suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("No conflict detected")
    print()


def multiple_tech_conflict():
    """
    Detect conflicts when proposing multiple technologies.
    """
    print("=" * 70)
    print("MULTIPLE TECHNOLOGY CONFLICT")
    print("=" * 70)
    print()

    checker = TechStackConflictChecker()

    class MockProject:
        tech_stack = ["Java", "MySQL", "Angular", "Kubernetes"]
        requirements = []
        goals = []
        constraints = []

    project = MockProject()
    print(f"Current tech stack: {project.tech_stack}")
    print()

    # Propose conflicting technologies
    new_insights = {
        "tech_stack": ["Node.js", "PostgreSQL"]
    }

    print(f"Proposed technologies: {new_insights['tech_stack']}")
    print()

    # Check for each proposed technology
    for tech in new_insights['tech_stack']:
        single_insight = {"tech_stack": [tech]}
        conflict = checker.check(
            insights=single_insight,
            project=project,
            current_user="Agent-ArchitectureReview"
        )

        if conflict:
            print(f"Conflict for {tech}:")
            print(f"  Severity: {conflict.severity}")
            print(f"  vs {conflict.old_value}")
        else:
            print(f"No conflict for {tech}")

    print()


if __name__ == "__main__":
    detect_tech_stack_conflict()
    print()
    multiple_tech_conflict()
    print("=" * 70)
