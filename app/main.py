from fastapi import FastAPI
from pydantic import BaseModel
from app.tools.field_applicability_tool import get_field_applicability
from app.tools.scoring_tool import estimate_visa_route
from app.tools.visa_rules_tool import lookup_visa_rule
from app.tools.checklist_tool import get_document_checklist
from app.security.guardrails import check_security_guardrails
from app.tools.country_tool import get_supported_countries, get_country_classification


app = FastAPI(title="VisaRoute Agent API")

@app.get("/")
def root():
    return {
        "status": "ok",
        "project": "VisaRoute Agent",
        "message": "Welcome to VisaRoute Agent API. Go to /docs or /health."
    }


class RouteRequest(BaseModel):
    passport_country: str
    source_country: str
    destination_country: str
    visa_purpose: str
    user_segment: str
    dependent_type: str = "not_applicable"
    travel_days_from_now: int
    previous_refusal: bool
    self_confidence: int
    budget_sensitivity: int
    corporate_support_available: bool


class ChecklistRequest(BaseModel):
    passport_country: str
    source_country: str
    destination_country: str
    visa_purpose: str
    user_segment: str = "general"
    dependent_type: str = "not_applicable"
    previous_refusal: bool = False


class GuardrailRequest(BaseModel):
    user_query: str

class FieldApplicabilityRequest(BaseModel):
    visa_purpose: str
    user_segment: str = "general"


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "VisaRoute Agent",
        "message": "API is running"
    }

@app.get("/countries")
def countries():
    return get_supported_countries()


@app.get("/countries/{country_name}")
def country_classification(country_name: str):
    return get_country_classification(country_name)

@app.post("/field-applicability")
def field_applicability(request: FieldApplicabilityRequest):
    return get_field_applicability(
        visa_purpose=request.visa_purpose,
        user_segment=request.user_segment
    )


@app.get("/visa-rule/{destination_country}")
def visa_rule(destination_country: str):
    return lookup_visa_rule(destination_country)


@app.post("/recommend")
def recommend_route(request: RouteRequest):
    return estimate_visa_route(
        passport_country=request.passport_country,
        source_country=request.source_country,
        dependent_type=request.dependent_type,
        visa_purpose=request.visa_purpose,
        destination_country=request.destination_country,
        user_segment=request.user_segment,
        travel_days_from_now=request.travel_days_from_now,
        previous_refusal=request.previous_refusal,
        self_confidence=request.self_confidence,
        budget_sensitivity=request.budget_sensitivity,
        corporate_support_available=request.corporate_support_available,
    )


@app.post("/checklist")
def checklist(request: ChecklistRequest):
    return get_document_checklist(
        passport_country=request.passport_country,
        source_country=request.source_country,
        destination_country=request.destination_country,
        visa_purpose=request.visa_purpose,
        user_segment=request.user_segment,
        dependent_type=request.dependent_type,
        previous_refusal=request.previous_refusal,
)


@app.post("/guardrail")
def guardrail(request: GuardrailRequest):
    return check_security_guardrails(request.user_query)
