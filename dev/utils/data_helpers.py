from dev.core.person import Person
from typing import List, Set

def append_ghost_persons(persons: List[Person]) -> List[Person]:
    existing_names: Set[str] = {p.name for p in persons}
    mentioned_targets: Set[str] = set()

    # Find all influence targets
    for person in persons:
        for influence in person.influences:
            mentioned_targets.add(influence.target)

    missing = mentioned_targets - existing_names
    ghost_persons = []

    for name in sorted(missing):
        ghost = Person(
            name=name,
            start="unknown",
            end="unknown",
            start_is_approx=True,
            influences=[],
            summary="Referenced as an influence but not included in timeline dataset.",
            school_of_thought=None,
            region=None,
            quotes=[],
            sources=[]
        )
        ghost_persons.append(ghost)

    return persons + ghost_persons
