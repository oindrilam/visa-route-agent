import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.tools.visa_rules_tool import lookup_visa_rule
from app.tools.scoring_tool import estimate_visa_route

def parse_bool(value: str) -> bool:
    return value.lower() in ["true", "yes", "y", "1"]


def main():
    parser = argparse.ArgumentParser(description="VisaRoute Agent demo runner")

    parser.add_argument("--destination", required=True)
    parser.add_argument("--purpose", required=True, choices=["tourist", "student", "business"])
    parser.add_argument("--segment", required=True)
    parser.add_argument("--days", type=int, required=True)
    parser.add_argument("--previous-refusal", default="false")
    parser.add_argument("--confidence", type=int, required=True)
    parser.add_argument("--budget-sensitivity", type=int, required=True)
    parser.add_argument("--corporate-support", default="false")

    args = parser.parse_args()

    visa_rule = lookup_visa_rule(args.destination)
    route = estimate_visa_route(
        visa_purpose=args.purpose,
        destination_country=args.destination,
        user_segment=args.segment,
        travel_days_from_now=args.days,
        previous_refusal=parse_bool(args.previous_refusal),
        self_confidence=args.confidence,
        budget_sensitivity=args.budget_sensitivity,
        corporate_support_available=parse_bool(args.corporate_support),
    )

    print("\n=== VisaRoute Agent Recommendation ===")
    print(f"Destination: {route['destination_country']}")
    print(f"Visa purpose: {route['visa_purpose']}")
    print(f"Visa category: {visa_rule.get('visa_category', 'Not available')}")
    print(f"Appointment required: {visa_rule.get('appointment_required', 'Unknown')}")
    print(f"Biometrics required: {visa_rule.get('biometrics_required', 'Unknown')}")
    print(f"Interview requirement: {route['interview_requirement']}")
    print(f"Estimated calendar days: {route['estimated_calendar_days']}")
    print(f"Self-apply effort hours: {route['self_apply_effort_hours']}")
    print(f"Assisted effort hours: {route['assisted_effort_hours']}")
    print(f"Assisted worth-it score: {route['assisted_worth_it_score']}/100")
    print(f"Recommendation: {route['recommendation']}")
    print(f"Note: {route['note']}")


if __name__ == "__main__":
    main()
