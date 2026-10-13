import re
from typing import Any
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class PortuguesePtJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://na-pt.org/sph/"
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
            "copyright": "",
        }

        # Extract date from qx-text-6112
        date_element = soup.find(id="qx-text-6112")
        if date_element:
            date_text = date_element.get_text().strip()
            # Extract just the date part, removing "MEDITAÇÃO DO DIA"
            match = re.search(r"(\w+,\s*\d+\s+de\s+\w+\s+de\s+\d+)", date_text)
            if match:
                result["date"] = match.group(1)

        # Extract title from h2 within qx-heading-5146
        heading_element = soup.find(id="qx-heading-5146")
        if heading_element:
            title_element = heading_element.select_one("h2 span")
            if title_element:
                result["title"] = title_element.get_text().strip()

        # Extract main content from qx-text-39245
        content_element = soup.find(id="qx-text-39245")
        if content_element:
            # Convert <br> tags to newlines before extracting text
            html_content = re.sub(r"<br\s*/?>", "\n", str(content_element))
            full_text = BeautifulSoup(html_content, "html.parser").get_text().strip()

            # Split into lines to look for quote pattern
            lines = full_text.split("\n")
            content_start_index = 0
            source_line_index = -1

            # Look for opening quote pattern: line ending with " followed by source line
            for i, raw_line in enumerate(lines):
                line = raw_line.strip()
                if re.search(r'"\s*$', line):
                    # Extract quoted text (everything before the trailing quote mark)
                    result["quote"] = re.sub(r'\s*"\s*$', "", line)

                    # Check next line for source
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line:
                            result["source"] = next_line
                            source_line_index = i + 1

                    content_start_index = (
                        source_line_index + 1 if source_line_index >= 0 else i + 1
                    )
                    break

            # Also check for enclosed quote pattern "text"
            if not result["quote"]:
                quote_match = re.search(r'"([^"]+)"', full_text)
                if quote_match:
                    result["quote"] = quote_match.group(1).strip()

                    # Remove quote from text to get remaining content
                    content_without_quote = re.sub(
                        r'"[^"]+"\s*', "", full_text, count=1
                    ).strip()

                    content_lines = content_without_quote.split("\n")
                    if content_lines:
                        first_line = content_lines[0].strip()
                        source_pattern = r"^[^.]+[,.]\s*\d+|^[^.]+,\s*p\."
                        if first_line and len(first_line) < 100 and re.search(source_pattern, first_line):
                            result["source"] = first_line
                            content_lines[0] = ""
                    lines = content_lines
                    content_start_index = 0

            # Collect content from content_start_index onward
            content_parts = [
                line.strip()
                for line in lines[content_start_index:]
                if line.strip()
            ]
            content_text = " ".join(content_parts)

            if content_text:
                result["content"] = [re.sub(r"\s+", " ", content_text).strip()]
            elif not result["quote"]:
                # No quote found, use entire content
                result["content"] = [re.sub(r"\s+", " ", full_text).strip()]

        # Extract "SÓ POR HOJE" section from qx-text-80201
        sph_element = soup.find(id="qx-text-80201")
        if sph_element:
            sph_text = sph_element.get_text().strip()
            # Remove "SÓ POR HOJE:" prefix
            thought = re.sub(r"^SÓ POR HOJE:\s*", "", sph_text)
            result["thought"] = re.sub(r"\s+", " ", thought).strip()

        # Extract copyright from qx-text-28340
        copyright_element = soup.find(id="qx-text-28340")
        if copyright_element:
            copyright_text = copyright_element.get_text().replace("\n", " ").strip()
            result["copyright"] = re.sub(r"\s+", " ", copyright_text).strip()

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
