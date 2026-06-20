"""
Parses arXiv Atom XML into structured Paper objects.
This version is namespace-safe and production-robust.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

from research_search.models.paper import Paper


ATOM = "{http://www.w3.org/2005/Atom}"


class ArxivParser:
    """
    Converts arXiv XML responses into structured Paper objects.
    """

    def parse(self, xml_data: str) -> List[Paper]:

        root = ET.fromstring(xml_data)

        papers: List[Paper] = []

        # IMPORTANT: correct way to handle default namespaces
        entries = root.findall(f".//{ATOM}entry")

        print(f"[DEBUG] Found entries: {len(entries)}")

        for entry in entries:

            paper_id = entry.find(f"{ATOM}id").text.split("/")[-1]
            title = entry.find(f"{ATOM}title").text.strip()
            abstract = entry.find(f"{ATOM}summary").text.strip()

            authors = [
                a.find(f"{ATOM}name").text
                for a in entry.findall(f"{ATOM}author")
            ]

            categories = [
                c.attrib["term"]
                for c in entry.findall(f"{ATOM}category")
            ]

            published = datetime.fromisoformat(
                entry.find(f"{ATOM}published").text.replace("Z", "+00:00")
            )

            updated_elem = entry.find(f"{ATOM}updated")
            updated = (
                datetime.fromisoformat(updated_elem.text.replace("Z", "+00:00"))
                if updated_elem is not None else None
            )

            url = entry.find(f"{ATOM}id").text

            print(f"Parsed paper: {paper_id} - {title[:60]}...")

            papers.append(
                Paper(
                    id=paper_id,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    categories=categories,
                    published=published,
                    updated=updated,
                    url=url,
                )
            )

        return papers