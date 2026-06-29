import json
from pathlib import Path
from typing import Dict, Any

from app.tools.visa_rules_tool import lookup_visa_rule


def get_document_checklist(
    visa_purpose: str,
    destination_country: str,
    previous_refusal: bool = False
) -> Dict[str, Any]:
    """Return an MVP document checklist for a visa purpose and destination."""

    data_path = Path(__file__).resolve().parents[1] / "data" / "document_rules.json"

    with open(data_path, "r", encoding="utf-8") as file:
        document_rules = json.load(file)

    purpose = visa_purpose.strip().lower()
    visa_rule = lookup_visa_rule(destination_country)

    if purpose not in document_rules:
        return {
            "found": False,
            "visa_purpose": visa_purpose,
            "destination_country": destination_country,
            "message": "Visa purpose is not available in MVP checklist dataset."
        }

    checklist = list(document_rules[purpose]["base_documents"])

    if previous_refusal:
        checklist.extend(document_rules[purpose]["risk_documents"])

    return {
        "found": True,
        "visa_purpose": purpose,
        "destination_country": destination_country,
        "visa_category": visa_rule.get("visa_category", "Not available"),
        "appointment_required": visa_rule.get("appointment_required", "Unknown"),
        "biometrics_required": visa_rule.get("biometrics_required", "Unknown"),
        "interview_requirement": visa_rule.get("interview_requirement", "Unknown"),
        "document_checklist": checklist,
        "document_count": len(checklist),
        "note": "This is an MVP checklist, not official visa advice. Verify with the official visa source."
    }
