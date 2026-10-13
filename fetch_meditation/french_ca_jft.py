from typing import List, Any
from datetime import datetime
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class FrenchCaJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://naquebec.org/juste-pour-aujourdhui/"
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, "html.parser")

        result = {
            "date": "",
            "quote": "",
            "source": "",
            "thought": "",
            "content": [],
            "title": "",
            "page": "",
            "copyright": f"Copyright (c) {datetime.now().year}, NA World Service, Inc. All Rights Reserved",
        }

        # The meditation is rendered inside a single Elementor loop item, which
        # scopes our queries away from the rest of the page (header, footer, etc.)
        item = soup.find("div", class_="e-loop-item")
        if item is None:
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

        # Extract the title (the day's heading, e.g. "Avoir raison")
        title_element = item.select_one("h1.elementor-heading-title")
        if title_element:
            result["title"] = title_element.get_text(strip=True)

        # The two text-editor widgets hold the date followed by the italic quote
        editors = item.select("div.elementor-widget-text-editor")
        if len(editors) >= 1:
            result["date"] = editors[0].get_text(strip=True)
        if len(editors) >= 2:
            result["quote"] = editors[1].get_text(strip=True)

        # The post content holds the source citation, the body paragraphs and the
        # closing "Juste pour aujourd'hui" thought, in that order.
        paragraphs = [
            p.get_text(strip=True)
            for p in item.select("div.elementor-widget-theme-post-content p")
            if p.get_text(strip=True)
        ]
        if len(paragraphs) >= 1:
            # First paragraph is the source (e.g. "Texte de base, p. 72")
            result["source"] = paragraphs[0]
        if len(paragraphs) >= 2:
            # Last paragraph is the closing thought
            result["thought"] = paragraphs[-1]
        # Whatever remains in between is the meditation body
        result["content"] = paragraphs[1:-1]

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
