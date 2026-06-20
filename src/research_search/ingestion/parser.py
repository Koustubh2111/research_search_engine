"""
This module is responsible for transforming raw arXiv XML into
structured internal Paper objects.

This is one of the most failure-prone parts of ingestion systems
because external data formats are never stable.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

from research_search.models.paper import Paper


class ArxivParser:
    """
    Converts arXiv XML responses into structured Paper objects.

    Key design rule:
    - NEVER return raw XML outside this module
    - Always normalize into internal schema (Paper)
    """

    def parse(self, xml_data: str) -> List[Paper]:
        """
        Parse arXiv XML into a list of Paper objects.

        Args:
            xml_data: raw XML string from arXiv API

        Returns:
            List of normalized Paper objects
        """

        root = ET.fromstring(xml_data)

        papers: List[Paper] = []

        # arXiv uses Atom feed format with namespaces
        namespace = {"atom": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("atom.entry", namespace):

            # Extract core fields safely
            paper_id = entry.find("atom:id", namespace).text.split("/")[-1]
            title = entry.find("atom:title", namespace).text.strip()
            abstract = entry.find("atom:summary", namespace).text.strip()

            # Authors are nested elements
            authors = [
                author.find("atom:name", namespace).text
                for author in entry.findall("atom:author", namespace)
            ]

            # Categories (multi-label classification)
            categories = [
                tag.attrib["term"]
                for tag in entry.findall("atom:category", namespace)
            ]

            # Publication timestamp
            published = datetime.fromisoformat(
                entry.find("atom:published", namespace).text.replace("Z", "+00:00")
            )

            updated_elem = entry.find("atom:updated", namespace)
            updated = (
                datetime.fromisoformat(updated_elem.text.replace("Z", "+00:00"))
                if updated_elem is not None
                else None
            )

            url = entry.find("atom:id", namespace).text

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