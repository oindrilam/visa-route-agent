import json
from pathlib import Path
from typing import Any, Dict, List


def _load_countries() -> Dict[str, Any]:
    """Load supported country master data for nationality, source, and destination dropdowns."""
    data_path = Path(__file__).resolve().parents[1] / "data" / "countries.json"

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_supported_countries() -> Dict[str, List[str]]:
    """Return supported countries grouped by core, Europe, Schengen, and all supported."""
    data = _load_countries()

    return {
        "core_countries": data["core_countries"],
        "european_countries": data["european_countries"],
        "schengen_countries": data["schengen_countries"],
        "non_schengen_european_countries": data["non_schengen_european_countries"],
        "all_supported_countries": data["all_supported_countries"],
    }


def get_country_classification(country_name: str) -> Dict[str, Any]:
    """Classify whether a country is supported, European, Schengen, or core."""
    data = _load_countries()
    country = country_name.strip()

    return {
        "country": country,
        "supported": country in data["all_supported_countries"],
        "is_core_country": country in data["core_countries"],
        "is_european": country in data["european_countries"],
        "is_schengen": country in data["schengen_countries"],
        "is_non_schengen_europe": country in data["non_schengen_european_countries"],
    }