from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class CalendarRepository:
    def __init__(self, events_file: str | Path) -> None:
        self.events_file = Path(events_file)

    def ensure_exists(self) -> None:
        """
        Ensure the parent directory exists.
        If the events file does not exist, create it with an empty structure.
        """
        self.events_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.events_file.exists():
            self._write_default_file()

    def get_events(self, max_events: int | None = None) -> list[dict[str, Any]]:
        """
        Load events from JSON, normalize them, sort them by start time,
        and optionally limit the returned number of events.
        """
        data = self._load_json()
        raw_events = data.get("events", [])

        if not isinstance(raw_events, list):
            return []

        normalized_events: list[dict[str, Any]] = []

        for event in raw_events:
            normalized = self._normalize_event(event)
            if normalized is not None:
                normalized_events.append(normalized)

        normalized_events.sort(key=lambda event: event["start_dt"])

        if max_events is not None:
            return normalized_events[:max_events]

        return normalized_events

    def has_events(self) -> bool:
        """Return True if at least one valid event exists."""
        return len(self.get_events()) > 0

    def reload(self, max_events: int | None = None) -> list[dict[str, Any]]:
        """Explicit alias for get_events(), useful from UI logic."""
        return self.get_events(max_events=max_events)

    def _load_json(self) -> dict[str, Any]:
        """
        Load the events JSON file.
        On any error, return an empty structure instead of raising.
        """
        try:
            with self.events_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {"events": []}

        if not isinstance(data, dict):
            return {"events": []}

        return data

    def _write_default_file(self) -> None:
        """Create a default empty events file."""
        default_data = {"events": []}

        with self.events_file.open("w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _normalize_event(self, event: Any) -> dict[str, Any] | None:
        """
        Normalize a single event entry.

        Expected input example:
        {
          "title": "Dentist appointment",
          "start": "2026-04-10T15:30:00",
          "end": "2026-04-10T16:00:00",
          "location": "Via Roma 10"
        }
        """
        if not isinstance(event, dict):
            return None

        title = str(event.get("title", "")).strip()
        start_raw = str(event.get("start", "")).strip()
        end_raw = str(event.get("end", "")).strip()
        location = str(event.get("location", "")).strip()

        if not title or not start_raw:
            return None

        start_dt = self._parse_datetime(start_raw)
        if start_dt is None:
            return None

        end_dt = self._parse_datetime(end_raw) if end_raw else None

        return {
            "title": title,
            "start": start_raw,
            "end": end_raw,
            "location": location,
            "start_dt": start_dt,
            "end_dt": end_dt,
            "display_time": self._format_display_time(start_dt, end_dt),
            "display_date": self._format_display_date(start_dt),
        }

    def _parse_datetime(self, value: str) -> datetime | None:
        """
        Parse a datetime string in ISO-like format.
        Supported examples:
          2026-04-10T15:30:00
          2026-04-10 15:30:00
          2026-04-10T15:30
          2026-04-10
        """
        candidates = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ]

        for fmt in candidates:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return None

    def _format_display_time(self, start_dt: datetime, end_dt: datetime | None) -> str:
        """
        Format a short human-readable time range.
        """
        start_str = start_dt.strftime("%H:%M")

        if end_dt is None:
            return start_str

        return f"{start_str} - {end_dt.strftime('%H:%M')}"

    def _format_display_date(self, start_dt: datetime) -> str:
        """
        Format a short human-readable date.
        Example: 10/04/2026
        """
        return start_dt.strftime("%d/%m/%Y")
