import json
from pathlib import Path
from typing import Any, Dict, List


SAFETY_DIMENSIONS = [
    "women_safety",
    "robbery_mugging",
    "pickpocketing",
    "violent_harm"
]


def _load_safety_sources() -> Dict[str, Any]:
    data_path = Path(__file__).resolve().parents[1] / "data" / "safety_sources.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def _get_safety_source_profile(destination_country: str) -> Dict[str, Any]:
    data = _load_safety_sources()
    return data.get(destination_country, data["default"])


def get_destination_safety_assessment(
    destination_country: str,
    visa_purpose: str,
    user_segment: str
) -> Dict[str, Any]:
    """
    Provides planning-level destination safety categories.

    This tool avoids blaming nationality, religion, ethnicity, or community.
    It separates general official crime data from traveler-specific evidence.
    """

    country = destination_country.strip()
    purpose = visa_purpose.strip().lower()
    profile = user_segment.strip().lower()
    source_profile = _get_safety_source_profile(country)

    count_status = source_profile.get("last_5_year_count_status", {})

    safety_categories: Dict[str, Dict[str, Any]] = {
        "women_safety": {
            "label": "Women safety",
            "planning_signal": "review_required",
            "last_5_year_count_status": count_status.get("women_safety", "source_review_required"),
            "traveler_specific_count_available": source_profile.get("traveler_specific_count_available", False),
            "what_to_check": [
                "solo travel advisories",
                "night travel guidance",
                "public transport safety",
                "harassment or assault warnings from official travel advisories"
            ]
        },
        "robbery_mugging": {
            "label": "Robbery / mugging",
            "planning_signal": "review_required",
            "last_5_year_count_status": count_status.get("robbery_mugging", "source_review_required"),
            "traveler_specific_count_available": source_profile.get("traveler_specific_count_available", False),
            "what_to_check": [
                "official robbery or mugging counts",
                "tourist robbery advisories",
                "street crime warnings",
                "high-risk city zones",
                "late-night movement guidance"
            ]
        },
        "pickpocketing": {
            "label": "Pickpocketing",
            "planning_signal": "review_required",
            "last_5_year_count_status": count_status.get("pickpocketing", "source_review_required"),
            "traveler_specific_count_available": source_profile.get("traveler_specific_count_available", False),
            "what_to_check": [
                "official theft or larceny data as a proxy",
                "crowded tourist-area warnings",
                "public transport theft warnings",
                "airport / station theft reports",
                "festival or event-related theft alerts"
            ]
        },
        "violent_harm": {
            "label": "Stabbing / shooting / death risk",
            "planning_signal": "review_required",
            "last_5_year_count_status": count_status.get("violent_harm", "source_review_required"),
            "traveler_specific_count_available": source_profile.get("traveler_specific_count_available", False),
            "what_to_check": [
                "official violent crime or homicide data",
                "official violent crime advisories",
                "terrorism or civil unrest advisories",
                "recent verified attacks affecting visitors, students, or workers",
                "emergency response guidance"
            ]
        }
    }

    profile_notes: List[str] = []

    if profile == "student":
        profile_notes.append("Check campus safety, student housing safety, and late-night commute guidance.")

    if profile in ["vp", "cxo", "business owner", "senior employee"]:
        profile_notes.append("Check business-district transport safety and hotel-to-meeting commute safety.")

    if purpose in ["work", "student", "dependent_family"]:
        profile_notes.append("Check neighborhood safety for long-stay accommodation, not only tourist zones.")

    return {
        "destination_country": country,
        "visa_purpose": purpose,
        "user_segment": profile,
        "safety_categories": safety_categories,
        "profile_notes": profile_notes,
        "source_mode": source_profile.get("source_mode", "framework_only"),
        "official_crime_data_sources": source_profile.get("official_crime_data_sources", []),
        "travel_advisory_sources": source_profile.get("travel_advisory_sources", []),
        "traveler_specific_count_available": source_profile.get("traveler_specific_count_available", False),
        "counting_rule": source_profile.get("counting_rule", ""),
        "source_confidence": "official_source_framework",
        "source_confidence_explanation": (
            "This version identifies official source families and last-5-year count availability. "
            "It does not invent exact crime counts unless an official dataset confirms the category, year, location, and victim group."
        ),
        "disclaimer": (
            "Planning signal only. This is not official safety advice. "
            "General crime counts must not be presented as tourist/student/visa-holder counts unless the source confirms that victim group."
        )
    }