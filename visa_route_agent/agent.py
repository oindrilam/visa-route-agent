from google.adk.agents.llm_agent import Agent
from app.tools.scoring_tool import estimate_visa_route
from app.tools.visa_rules_tool import lookup_visa_rule


def get_project_status() -> dict:
    """Returns current VisaRoute Agent MVP status."""
    return {
        "status": "success",
        "project": "VisaRoute Agent",
        "mvp_scope": "Indian passport holders applying for tourist, student, or business visas",
        "tools_available": [
            "get_project_status",
            "lookup_visa_rule",
            "estimate_visa_route"
        ],
        "next_build_step": "Add document checklist logic"
    }


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="visa_route_agent",
    description="A visa route optimizer for Indian passport holders.",
    instruction="""
You are VisaRoute Agent.

You help Indian passport holders estimate the best visa application route.

Use lookup_visa_rule when the user asks about destination visa process, appointment,
biometrics, interview, or official channel.

Use estimate_visa_route when the user gives visa purpose, destination, role/profile,
travel urgency, previous refusal status, confidence, budget sensitivity, and corporate support.

Always say this is planning guidance, not official visa advice.
""",
    tools=[get_project_status, lookup_visa_rule, estimate_visa_route],
)
