# core/event.py

from dataclasses import dataclass, field
from typing import Optional, List
from uuid import uuid4

@dataclass
class Event:
    name: str
    start_year: int

    id: str = field(default_factory=lambda: str(uuid4()))
    end_year: Optional[int] = None
    description: str = ""
    scope: str = "local"  # "local", "major", "global"
    type: str = "generic"  # e.g., war, discovery, birth, etc.
    region: Optional[str] = None
    related_to: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        if "name" not in data:
            raise ValueError("Missing 'name' for event.")
        if "start_year" not in data or not isinstance(data["start_year"], int):
            raise ValueError(f"Missing or invalid 'start_year' for event '{data.get('name', '?')}'.")

        scope = data.get("scope", "local")
        if scope not in {"local", "major", "global"}:
            raise ValueError(f"Invalid scope '{scope}' for event '{data['name']}'.")

        end_year = data.get("end_year")
        if end_year is not None and not isinstance(end_year, int):
            raise ValueError(f"Invalid 'end_year' for event '{data['name']}'.")

        related_to = data.get("related_to", [])
        if not isinstance(related_to, list):
            raise ValueError(f"'related_to' must be a list for event '{data['name']}'.")

        return cls(
            name=data["name"],
            start_year=data["start_year"],
            end_year=end_year,
            description=data.get("description", ""),
            scope=scope,
            type=data.get("type", "generic"),
            region=data.get("region"),
            related_to=related_to
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "description": self.description,
            "scope": self.scope,
            "type": self.type,
            "region": self.region,
            "related_to": self.related_to
        }
