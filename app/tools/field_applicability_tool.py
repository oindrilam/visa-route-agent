from typing import Any, Dict, List


ROLE_OPTIONS_BY_PURPOSE = {
    "tourist": [
        "general",
        "student",
        "employee",
        "senior employee",
        "VP",
        "CXO",
        "business owner",
        "homemaker",
        "minor",
        "retired"
    ],
    "business": [
        "employee",
        "senior employee",
        "VP",
        "CXO",
        "business owner"
    ],
    "student": [
        "student"
    ],
    "work": [
        "employee",
        "senior employee",
        "VP",
        "CXO"
    ],
    "dependent_family": [
        "spouse",
        "child",
        "parent",
        "family visitor"
    ],
    "transit": [
        "general",
        "student",
        "employee",
        "business owner"
    ]
}


DEPENDENT_TYPES_BY_PURPOSE = {
    "dependent_family": [
        "spouse",
        "child",
        "parent",
        "family_visitor",
        "dependent_of_student",
        "dependent_of_worker"
    ]
}


def get_field_applicability(visa_purpose: str, user_segment: str = "general") -> Dict[str, Any]:
    """Return frontend field applicability rules based on visa purpose and profile."""

    purpose = visa_purpose.strip().lower()
    role = user_segment.strip().lower()

    role_options: List[str] = ROLE_OPTIONS_BY_PURPOSE.get(
        purpose,
        ROLE_OPTIONS_BY_PURPOSE["tourist"]
    )

    corporate_support_applicable = purpose in ["business", "work"]
    dependent_type_applicable = purpose == "dependent_family"

    return {
        "visa_purpose": purpose,
        "user_segment": role,
        "role_options": role_options,
        "corporate_support_applicable": corporate_support_applicable,
        "dependent_type_applicable": dependent_type_applicable,
        "dependent_type_options": DEPENDENT_TYPES_BY_PURPOSE.get(purpose, ["not_applicable"]),
        "disabled_fields": {
            "corporate_support_available": not corporate_support_applicable,
            "dependent_type": not dependent_type_applicable
        },
        "captions": {
            "corporate_support_available": (
                "Corporate support: Not applicable for selected visa purpose."
                if not corporate_support_applicable else ""
            ),
            "dependent_type": (
                "Dependent / family type: Not applicable for selected visa purpose."
                if not dependent_type_applicable else ""
            )
        }
    }