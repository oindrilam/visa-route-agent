from typing import Any, Dict, List


SAFETY_DIMENSIONS = [
    "women_safety",
    "robbery_mugging",
    "pickpocketing",
    "violent_harm"
]


def get_destination_safety_assessment(
    destination_country: str,
    visa_purpose: str,
    user_segment: str
) -> Dict[str, Any]:
    """
    Provides planning-level destination safety categories.

    This tool intentionally avoids blaming any nationality, religion, ethnicity,
    or community. It focuses only on traveler-relevant risk categories and
    source confidence.
    """

    country = destination_country.strip()
    purpose = visa_purpose.strip().lower()
    profile = user_segment.strip().lower()

    safety_categories: Dict[str, Dict[str, Any]] = {
        "women_safety": {
            "label": "Women safety",
            "planning_signal": "review_required",
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
            "what_to_check": [
                "tourist robbery advisories",
                "street crime warnings",
                "high-risk city zones",
                "late-night movement guidance"
            ]
        },
        "pickpocketing": {
            "label": "Pickpocketing",
            "planning_signal": "review_required",
            "what_to_check": [
                "crowded tourist-area warnings",
                "public transport theft warnings",
                "airport / station theft reports",
                "festival or event-related theft alerts"
            ]
        },
        "violent_harm": {
            "label": "Stabbing / shooting / death risk",
            "planning_signal": "review_required",
            "what_to_check": [
                "official violent crime advisories",
                "terrorism or civil unrest advisories",
                "recent verified attacks affecting visitors, students, or workers",
                "emergency response guidance"
            ]
        }
    }

    profile_notes: List[str] = []

    if profile in ["student"]:
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
        "source_confidence": "framework_only",
        "source_confidence_explanation": (
            "This version provides a safety-assessment framework. "
            "Verified official advisories and recent incident sources should be checked before final travel decisions."
        ),
        "disclaimer": (
            "Planning signal only. This is not official safety advice. "
            "Do not use this to make discriminatory conclusions about any group or community."
        )
    }