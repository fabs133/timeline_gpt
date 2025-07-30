import json
from typing import List, Optional

SCHEMA_INSTRUCTIONS = """
Please return the data in the following JSON format and provide it as a downloadable .json file named 'generated_timeline.json':

{
  "metadata": {
    "version": "1.0",
    "created": "<date>",
    "source": "AI generated"
  },
  "persons": [
    {
      "name": "string",
      "start": "int or 'circa -###'",
      "end": "int",
      "start_is_approx": "bool",
      "influences": [
        { "target": "string", "type": "string", "certainty": "string" }
      ],
      "summary": "string",
      "school_of_thought": "string",
      "region": "string",
      "quotes": ["string", "..."],
      "sources": ["string", "..."]
    }
  ],
  "events": [
    {
      "name": "string",
      "start_year": "int",
      "end_year": "int (optional)",
      "description": "string",
      "scope": "local | major | global",
      "type": "string",
      "region": "string",
      "related_to": ["string", "..."]
    }
  ]
}
"""

class PromptGenerator:
    def __init__(self, data):
        self.persons = data.get("persons", [])
        self.events = data.get("events", [])

    def generate(self, mode: str, start_year: int, end_year: int,
                 selected_people: Optional[List[str]] = None,
                 selected_events: Optional[List[str]] = None,
                 detail_level: str = "medium",
                 filters: Optional[dict] = None) -> str:

        if mode == "timeline":
            body = self._generate_timeline_prompt(start_year, end_year, selected_people, selected_events, detail_level, filters)
        elif mode == "influence_network":
            body = self._generate_influence_prompt(start_year, end_year, selected_people, selected_events, detail_level, filters)
        elif mode == "biographical_summaries":
            body = self._generate_bio_prompt(selected_people, detail_level, filters)
        elif mode == "event_chronology":
            body = self._generate_event_chronology_prompt(start_year, end_year, selected_events, detail_level, filters)
        elif mode == "philosophical_theme":
            body = self._generate_theme_prompt(
                theme=filters.get("theme", [None])[0] if filters else None,
                start_year=start_year,
                end_year=end_year,
                selected_people=selected_people,
                selected_events=selected_events,
                detail_level=detail_level,
                filters=filters
            )
        else:
            raise ValueError(f"Unknown mode: {mode}")

        return f"{SCHEMA_INSTRUCTIONS}\n\n{body}"

    def _generate_theme_prompt(self, theme, start_year, end_year, selected_people, selected_events, detail_level, filters):
        if not theme:
            raise ValueError("Theme must be provided for philosophical_theme mode.")

        people_to_use = selected_people or [
            p["name"] for p in self.persons
            if not filters or (
                ("region" not in filters or p.get("region") in filters["region"]) and
                ("school_of_thought" not in filters or p.get("school_of_thought") in filters["school_of_thought"])
            )
        ]

        events_to_use = selected_events or [
            e["name"] for e in self.events
            if not filters or (
                ("region" not in filters or e.get("region") in filters["region"]) and
                ("event_type" not in filters or e.get("type") in filters["event_type"])
            )
        ]

        people_str = ', '.join(people_to_use)
        events_str = ', '.join(events_to_use)

        body = f"""Explore the philosophical theme of \"{theme}\" between the years {start_year} and {end_year}.

Consider the following thinkers and figures:
{people_str or 'Relevant historical philosophers and political leaders'}

And the following events:
{events_str or 'Key cultural, military, or political events'}

For each, explain how their ideas, actions, or impact reflected, challenged, or shaped the theme of \"{theme}\".

Discuss:
- How the theme evolved or was debated across time
- Whether consensus or contradiction emerged
- How the theme’s interpretation varied by region or ideology

Aim for {detail_level} detail."""

        return self._append_filters(body, filters)

    def _generate_timeline_prompt(self, start_year, end_year, selected_people, selected_events, detail_level, filters):
        people_str = ', '.join(selected_people or [])
        events_str = ', '.join(selected_events or [])

        body = f"""Create a historical timeline between {start_year} and {end_year} CE/BCE.
Include these figures: {people_str or 'any major philosophers active during that time'}.
Include important events such as: {events_str or 'major cultural or military events'}.
Please explain how historical context influenced these thinkers. Aim for {detail_level} detail."""

        return self._append_filters(body, filters)

    def _generate_influence_prompt(self, start_year, end_year, selected_people, selected_events, detail_level, filters):
        people_str = ', '.join(selected_people or [])
        events_str = ', '.join(selected_events or [])

        body = f"""Generate an intellectual influence map for the following philosophers: {people_str}.
Describe how they influenced each other and how events like {events_str} shaped their thinking.
Include timelines and descriptions of key interactions or transitions. Aim for {detail_level} detail."""

        return self._append_filters(body, filters)

    def _generate_bio_prompt(self, selected_people, detail_level, filters):
        people_str = ', '.join(selected_people or [])

        body = f"""Provide concise biographical summaries for: {people_str}.
Highlight their time period, school of thought, and any influences or events that shaped them.
Use a readable tone and keep it at a {detail_level} level of depth."""

        return self._append_filters(body, filters)

    def _generate_event_chronology_prompt(self, start_year, end_year, selected_events, detail_level, filters):
        events_to_use = selected_events or [
            e["name"] for e in self.events
            if not filters or (
                ("region" not in filters or e.get("region") in filters["region"]) and
                ("event_type" not in filters or e.get("type") in filters["event_type"])
            )
        ]

        events_sorted = sorted(
            [e for e in self.events if e["name"] in events_to_use],
            key=lambda x: x.get("start_year", 0)
        )

        body = f"""Chronologically describe the following events between {start_year} and {end_year} CE/BCE:

"""
        for event in events_sorted:
            name = event["name"]
            start = event["start_year"]
            end = event.get("end_year")
            desc = event.get("description", "").strip()

            year_info = f"{start}" if not end else f"{start}–{end}"
            body += f"- {name} ({year_info})\n"
            if desc:
                body += f"  Context: {desc}\n"

        body += f"""
For each event, address the following:
- What were the historical causes and tensions leading up to it?
- What occurred during the event?
- What were the short- and long-term consequences?

Aim for {detail_level} detail in each explanation.
"""
        return self._append_filters(body, filters)

    def _append_filters(self, body: str, filters: Optional[dict]) -> str:
        if filters:
            filter_notes = [f"{k.replace('_', ' ')}: {', '.join(v)}" for k, v in filters.items() if v]
            if filter_notes:
                body += "\n\nApply the following filters:\n" + "\n".join(f"- {line}" for line in filter_notes)
        return body

def load_data(path="dev/schema.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
