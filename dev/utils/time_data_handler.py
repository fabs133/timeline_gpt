from dev.core.person import Person
from dev.core.event import Event
from typing import List, Set
import json

class TimelineDataHandler:
    def __init__(self, package_path):
        self.package_path = package_path
        self.persons = []
        self.events = []

    def load(self):
        # Load people
        with open(self.package_path) as f:
            raw = json.load(f)
        self.persons = [Person.from_dict(p) for p in raw["persons"]]
        self.events = [Event.from_dict(e) for e in raw.get("events", [])]

        return self.persons, self.events

    def validate_context(self):
        names = set()
        for person in self.persons:
            if person.name in names:
                raise ValueError(f"Duplicate name found: {person.name}")
            names.add(person.name)

        all_names = {p.name for p in self.persons}
        for person in self.persons:
            for influencee in person.influenced:
                if influencee not in all_names:
                    raise ValueError(f"{person.name} lists unknown influencee: {influencee}")

        name_to_person = {p.name: p for p in self.persons}
        for person in self.persons:
            person_end = person.parsed_end()
            for influencee in person.influenced:
                target = name_to_person[influencee]
                target_start = target.parsed_start()

                if person_end is None or target_start is None:
                    print(f"⚠️  Cannot validate dates for {person.name} → {target.name} due to uncertain years.")
                    continue

                gap = target_start - person_end
                if gap > 0:
                    print(f"⚠️  Note: {person.name} died {gap} years before {target.name} was born.")
                elif gap < -20:
                    print(f"⚠️  Note: {person.name} still alive {abs(gap)} years after {target.name} was born — "
                        f"consider rechecking chronology.")
