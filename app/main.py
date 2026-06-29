from fastapi import FastAPI
from pydantic import BaseModel

from app.tools.scoring_tool import estimate_visa_route
from app.tools.visa_rules_tool import lookup_visa_rule
from app.tools.checklist_tool import get_document_checklist
from app.security.guardrails import check_security_guardrails


app = FastAPI(title="VisaRoute Agent API")

@app.get("/")
def root():
    return {
        "status": "ok",
        "project": "VisaRoute Agent",
        "message": "Welcome to VisaRoute Agent API. Go to /docs or /health."
    }


class RouteRequest(BaseModel):
    visa_purpose: str
    destination_country: str
    user_segment: str
    travel_days_from_now: int
    previous_refusal: bool
    self_confidence: int
    budget_sensitivity: int
    corporate_support_available: bool


class ChecklistRequest(BaseModel):
    visa_purpose: str
    destination_country: str
    previous_refusal: bool = False


class GuardrailRequest(BaseModel):
    user_query: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "VisaRoute Agent",
        "message": "API is running"
    }


@app.get("/visa-rule/{destination_country}")
def visa_rule(destination_country: str):
    return lookup_visa_rule(destination_country)


@app.post("/recommend")
def recommend_route(request: RouteRequest):
    return estimate_visa_route(
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
        visa_purpose=request.visa_purpose,
        destination_country=request.destination_country,
        previous_refusal=request.previous_refusal,
    )


@app.post("/guardrail")
def guardrail(request: GuardrailRequest):
    return check_security_guardrails(request.user_query)
