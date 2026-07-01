import json
from pathlib import Path
from typing import Any, Dict


SCHENGEN_COUNTRIES = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic", "Denmark",
    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
    "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
    "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Switzerland"
}


def _load_source_links() -> Dict[str, Any]:
    data_path = Path(__file__).resolve().parents[1] / "data" / "source_links.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_source_links(destination_country: str) -> Dict[str, Any]:
    """Return official and authorized visa source links for a destination."""

    country = destination_country.strip()
    data = _load_source_links()

    lookup_key = "Schengen" if country in SCHENGEN_COUNTRIES else country
    source_data = data.get(lookup_key)

    if not source_data:
        return {
            "destination_country": country,
            "source_key": lookup_key,
            "available": False,
            "message": "No official source links configured yet for this destination.",
            "official_links": [],
            "authorized_service_links": []
        }

    return {
        "destination_country": country,
        "source_key": lookup_key,
        "available": True,
        **source_data,
        "disclaimer": "Always verify visa rules on the official government website before applying."
    }