from typing import Dict, Any


def estimate_visa_route(
    visa_purpose: str,
    destination_country: str,
    user_segment: str,
    travel_days_from_now: int,
    previous_refusal: bool,
    self_confidence: int,
    budget_sensitivity: int,
    corporate_support_available: bool
) -> Dict[str, Any]:
    """Estimate visa route, effort, calendar days, and assisted-service worth-it score."""

    purpose = visa_purpose.lower()
    segment = user_segment.lower()

    purpose_rules = {
        "tourist": {
            "complexity": 30,
            "document_prep_days": 3,
            "processing_days": 15,
            "self_effort_hours": 8,
            "interview": "Usually not required, but may be requested",
            "biometrics": "Depends on destination"
        },
        "student": {
            "complexity": 70,
            "document_prep_days": 12,
            "processing_days": 30,
            "self_effort_hours": 22,
            "interview": "May be required",
            "biometrics": "Often required"
        },
        "business": {
            "complexity": 45,
            "document_prep_days": 5,
            "processing_days": 15,
            "self_effort_hours": 10,
            "interview": "May be required",
            "biometrics": "Depends on destination"
        }
    }

    rule = purpose_rules.get(purpose, purpose_rules["tourist"])

    urgency_score = 30 if travel_days_from_now <= 15 else 20 if travel_days_from_now <= 30 else 10 if travel_days_from_now <= 60 else 0
    time_value_score = 25 if "vp" in segment or "cxo" in segment else 15 if "senior" in segment else 8
    refusal_score = 25 if previous_refusal else 0
    corporate_support_score = -15 if corporate_support_available else 0

    assisted_score = (
        urgency_score
        + int(rule["complexity"] * 0.4)
        + time_value_score
        + refusal_score
        - int(self_confidence * 3)
        - int(budget_sensitivity * 2)
        + corporate_support_score
    )

    assisted_score = max(0, min(100, assisted_score))

    appointment_wait_days = 7 if rule["complexity"] < 50 else 14
    buffer_days = 7
    calendar_days = rule["document_prep_days"] + appointment_wait_days + rule["processing_days"] + buffer_days
    assisted_effort_hours = max(3, rule["self_effort_hours"] - 5)

    if purpose == "business" and corporate_support_available:
        recommendation = "Use corporate travel desk with personal presence for mandatory steps"
    elif assisted_score >= 75:
        recommendation = "Use expert or assisted visa support"
    elif assisted_score >= 55:
        recommendation = "Use assisted platform if budget allows"
    elif previous_refusal:
        recommendation = "Get expert review before applying"
    else:
        recommendation = "Self-apply with checklist guidance"

    return {
        "destination_country": destination_country,
        "visa_purpose": visa_purpose,
        "estimated_calendar_days": calendar_days,
        "self_apply_effort_hours": rule["self_effort_hours"],
        "assisted_effort_hours": assisted_effort_hours,
        "interview_requirement": rule["interview"],
        "biometrics_requirement": rule["biometrics"],
        "assisted_worth_it_score": assisted_score,
        "recommendation": recommendation,
        "note": "This is an MVP planning estimate, not official visa advice."
    }
