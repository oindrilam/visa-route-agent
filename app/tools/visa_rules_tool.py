import json
from pathlib import Path
from typing import Dict, Any


def lookup_visa_rule(destination_country: str) -> Dict[str, Any]:
    """Look up MVP visa rule information for a destination country."""

    data_path = Path(__file__).resolve().parents[1] / "data" / "visa_rules.json"

    with open(data_path, "r", encoding="utf-8") as file:
        rules = json.load(file)

    country = destination_country.strip().title()

    if country not in rules:
        return {
            "found": False,
            "destination_country": destination_country,
            "message": "Destination is not available in MVP dataset yet."
        }

    return {
        "found": True,
        "destination_country": country,
        **rules[country]
    }
