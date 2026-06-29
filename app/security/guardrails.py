from typing import Dict, Any


BLOCKED_PATTERNS = [
    "fake document",
    "fake bank statement",
    "fake invitation letter",
    "fake salary slip",
    "fake employment letter",
    "forge",
    "forged",
    "fraud",
    "lie in visa application",
    "hide previous refusal",
    "bypass biometrics",
    "bypass interview",
    "guarantee visa approval",
    "make fake bank statement"
]


def check_security_guardrails(user_query: str) -> Dict[str, Any]:
    """Basic security guardrail for visa guidance requests."""

    query = user_query.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in query:
            return {
                "allowed": False,
                "risk_type": "unsafe_or_fraudulent_visa_request",
                "matched_pattern": pattern,
                "message": "I cannot help with fake documents, hiding refusals, bypassing mandatory steps, or guaranteeing visa approval. I can help you prepare a truthful checklist and safer application plan."
            }

    return {
        "allowed": True,
        "risk_type": "none",
        "matched_pattern": None,
        "message": "Request passed MVP security guardrail."
    }
