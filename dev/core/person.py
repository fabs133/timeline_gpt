# core/person.py

from dataclasses import dataclass, field
from typing import List, Optional, Union, Tuple
from uuid import uuid4

@dataclass
class Influence:
    target: str
    type: Optional[str] = None
    certainty: Optional[str] = None

@dataclass
class Person:
    name: str
    start: Union[int, str]
    end: Union[int, str]

    id: str = field(default_factory=lambda: str(uuid4()))
    start_is_approx: bool = False
    influences: List[Influence] = field(default_factory=list)
    summary: str = ""

    # Optional fields
    school_of_thought: Optional[str] = None
    region: Optional[str] = None
    quotes: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)


    @classmethod
    def from_dict(cls, data: dict):
        if "name" not in data:
            raise ValueError("Missing 'name' for person.")
        if "start" not in data:
            raise ValueError(f"Missing 'start' for person '{data.get('name', '?')}'.")
        if "end" not in data:
            raise ValueError(f"Missing 'end' for person '{data.get('name', '?')}'.")

        start_value, is_approx = cls._parse_year_with_flag_static(data["start"])
        influences_data = data.get("influences", [])
        influences = [Influence(**inf) for inf in influences_data]

        return cls(
            name=data["name"],
            start=data["start"],
            end=data["end"],
            start_is_approx=is_approx,
            influences=influences,
            summary=data.get("summary", ""),
            school_of_thought=data.get("school_of_thought"),
            region=data.get("region"),
            quotes=data.get("quotes", []),
            sources=data.get("sources", [])
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "start_is_approx": self.start_is_approx,
            "influences": [inf.__dict__ for inf in self.influences],
            "summary": self.summary,
            "school_of_thought": self.school_of_thought,
            "region": self.region,
            "quotes": self.quotes,
            "sources": self.sources
        }

    def parsed_start(self) -> Optional[int]:
        return self._parse_year(self.start)

    def parsed_end(self) -> Optional[int]:
        return self._parse_year(self.end)

    def _parse_year(self, value: Union[int, str]) -> Optional[int]:
        result, _ = self._parse_year_with_flag(value)
        return result

    def _parse_year_with_flag(self, value: Union[int, str]) -> Tuple[Optional[int], bool]:
        return self._parse_year_with_flag_static(value)

    @staticmethod
    def _parse_year_with_flag_static(value: Union[int, str]) -> Tuple[Optional[int], bool]:
        if isinstance(value, int):
            return value, False
        if isinstance(value, str):
            if "circa" in value.lower():
                year = value.lower().replace("circa", "").strip()
                try:
                    return int(year), True
                except ValueError:
                    return None, True
            try:
                return int(value), False
            except ValueError:
                return None, False
        return None, False
