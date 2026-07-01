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

    # 1. Load the JSON file
    data = _load_safety_sources()
    display_labels = data.get("display_labels", {})
    countries = data.get("countries", {})
    disclaimer = data.get(
        "disclaimer",
        "Planning signal only. This is not official safety advice. "
        "General crime counts must not be presented as tourist/student/visa-holder counts unless the source confirms that victim group."
    )

    # 3. For the selected destination country, read from countries[country_name]
    country_data = countries.get(country)

    if country_data is not None:
        # Country is found
        last_5_year_count_status = country_data.get("last_5_year_count_status")
        if not last_5_year_count_status:
            if country == "Ukraine":
                last_5_year_count_status = "conflict_or_war_risk_context_needed"
            else:
                last_5_year_count_status = "official_general_count_possible"

        traveler_specific_count_status = country_data.get("traveler_specific_count_status")
        if not traveler_specific_count_status:
            traveler_specific_count_status = "traveler_specific_not_confirmed"

        proxy_status = country_data.get("proxy_status")
        if not proxy_status:
            proxy_status = "proxy_possible_using_theft_or_larceny_categories"

        official_crime_statistics_sources = country_data.get("official_crime_statistics_sources", [])
        traveler_safety_advisory_sources = country_data.get("traveler_safety_advisory_sources", [])
    else:
        # 8. If a country is not found, return empty source arrays and safe default labels
        last_5_year_count_status = "official_stats_need_manual_verification"
        traveler_specific_count_status = "traveler_specific_not_confirmed"
        proxy_status = "official_stats_need_manual_verification"
        official_crime_statistics_sources = []
        traveler_safety_advisory_sources = []

    # 6. Label logic should be display_labels.get(machine_value, machine_value)
    last_5_year_count_label = display_labels.get(last_5_year_count_status, last_5_year_count_status)
    traveler_specific_count_label = display_labels.get(traveler_specific_count_status, traveler_specific_count_status)
    proxy_status_label = display_labels.get(proxy_status, proxy_status)

    traveler_specific_count_available = (traveler_specific_count_status == "official_traveler_specific_possible")

    # Safety categories structure
    safety_categories: Dict[str, Dict[str, Any]] = {
        "women_safety": {
            "label": "Women safety",
            "planning_signal": "review_required",
            "last_5_year_count_status": last_5_year_count_status,
            "last_5_year_count_label": last_5_year_count_label,
            "traveler_specific_count_available": traveler_specific_count_available,
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
            "last_5_year_count_status": last_5_year_count_status,
            "last_5_year_count_label": last_5_year_count_label,
            "traveler_specific_count_available": traveler_specific_count_available,
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
            "last_5_year_count_status": last_5_year_count_status,
            "last_5_year_count_label": last_5_year_count_label,
            "traveler_specific_count_available": traveler_specific_count_available,
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
            "last_5_year_count_status": last_5_year_count_status,
            "last_5_year_count_label": last_5_year_count_label,
            "traveler_specific_count_available": traveler_specific_count_available,
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
        "source_mode": "framework_only" if country_data is None else country_data.get("source_mode", "framework_only"),
        "official_crime_data_sources": official_crime_statistics_sources,
        "travel_advisory_sources": traveler_safety_advisory_sources,
        "official_crime_statistics_sources": official_crime_statistics_sources,
        "traveler_safety_advisory_sources": traveler_safety_advisory_sources,
        "last_5_year_count_status": last_5_year_count_status,
        "traveler_specific_count_status": traveler_specific_count_status,
        "proxy_status": proxy_status,
        "last_5_year_count_label": last_5_year_count_label,
        "traveler_specific_count_label": traveler_specific_count_label,
        "proxy_status_label": proxy_status_label,
        "traveler_specific_count_available": traveler_specific_count_available,
        "counting_rule": "Only label a number as traveler-specific when the source explicitly identifies the victim group as tourists, students, visa holders, or foreign workers." if country_data is None else country_data.get("counting_rule", ""),
        "source_confidence": "official_source_framework",
        "source_confidence_explanation": (
            "This version identifies official source families and last-5-year count availability. "
            "It does not invent exact crime counts unless an official dataset confirms the category, year, location, and victim group."
        ),
        "disclaimer": disclaimer
    }