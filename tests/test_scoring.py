from app.tools.scoring_tool import estimate_visa_route


def test_business_vp_with_corporate_support_recommends_corporate_desk():
    result = estimate_visa_route(
        visa_purpose="business",
        destination_country="Germany",
        user_segment="VP",
        travel_days_from_now=20,
        previous_refusal=False,
        self_confidence=4,
        budget_sensitivity=2,
        corporate_support_available=True,
    )

    assert result["recommendation"] == "Use corporate travel desk with personal presence for mandatory steps"
    assert result["estimated_calendar_days"] == 34
    assert result["self_apply_effort_hours"] == 10
    assert result["assisted_effort_hours"] == 5


def test_student_visa_has_higher_effort_and_longer_calendar_days():
    result = estimate_visa_route(
        visa_purpose="student",
        destination_country="USA",
        user_segment="student",
        travel_days_from_now=45,
        previous_refusal=False,
        self_confidence=5,
        budget_sensitivity=5,
        corporate_support_available=False,
    )

    assert result["estimated_calendar_days"] == 63
    assert result["self_apply_effort_hours"] == 22
    assert result["interview_requirement"] == "May be required"
    assert result["biometrics_requirement"] == "Often required"


def test_tourist_confident_user_can_self_apply():
    result = estimate_visa_route(
        visa_purpose="tourist",
        destination_country="Dubai",
        user_segment="salaried employee",
        travel_days_from_now=90,
        previous_refusal=False,
        self_confidence=9,
        budget_sensitivity=8,
        corporate_support_available=False,
    )

    assert result["recommendation"] == "Self-apply with checklist guidance"
    assert result["assisted_worth_it_score"] < 55


def test_previous_refusal_increases_assisted_score():
    without_refusal = estimate_visa_route(
        visa_purpose="tourist",
        destination_country="UK",
        user_segment="salaried employee",
        travel_days_from_now=40,
        previous_refusal=False,
        self_confidence=5,
        budget_sensitivity=5,
        corporate_support_available=False,
    )

    with_refusal = estimate_visa_route(
        visa_purpose="tourist",
        destination_country="UK",
        user_segment="salaried employee",
        travel_days_from_now=40,
        previous_refusal=True,
        self_confidence=5,
        budget_sensitivity=5,
        corporate_support_available=False,
    )

    assert with_refusal["assisted_worth_it_score"] > without_refusal["assisted_worth_it_score"]
