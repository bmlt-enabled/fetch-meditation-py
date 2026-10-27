import json
from typing import Any
from datetime import datetime
import pytz
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class DanishJft:
    # The feed labels each entry with a Danish month name rather than a number,
    # so we map the current month onto the same spelling to find today's entry.
    MONTHS = {
        1: "januar",
        2: "februar",
        3: "marts",
        4: "april",
        5: "maj",
        6: "juni",
        7: "juli",
        8: "august",
        9: "september",
        10: "oktober",
        11: "november",
        12: "december",
    }

    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://www.nadanmark.dk/jft.json"
        response = HttpUtility.http_get(url)
        entries = json.loads(response)

        result = {
            "date": "",
            "quote": "",
            "source": "",
            "thought": "",
            "content": [],
            "title": "",
            "page": "",
            "copyright": f"Copyright (c) {datetime.now().year}, NA World Services, Inc. All Rights Reserved",
        }

        # The feed carries the whole year, so we pick out today's entry locally,
        # honoring the configured time zone when deciding what "today" is.
        if getattr(self.settings, "time_zone", None):
            now = datetime.now(pytz.timezone(self.settings.time_zone))
        else:
            now = datetime.now()
        day = now.day
        month = DanishJft.MONTHS[now.month]

        today = None
        for entry in entries:
            try:
                entry_day = int(entry.get("day", 0))
            except (TypeError, ValueError):
                entry_day = 0
            if entry_day == day and entry.get("month", "") == month:
                today = entry
                break

        if today is not None:
            result["date"] = f"{today.get('day', '')}. {today.get('month', '')}".strip()
            result["title"] = today.get("title", "")
            result["quote"] = today.get("quote", "")
            result["source"] = today.get("source", "")
            result["thought"] = today.get("jft", "")
            # The body arrives as a single string with newline-separated paragraphs.
            result["content"] = [
                line.strip() for line in today.get("text", "").split("\n") if line.strip()
            ]

        return JftEntry(
            result["date"],
            result["title"],
            result["page"],
            result["quote"],
            result["source"],
            result["content"],
            result["thought"],
            result["copyright"],
        )
