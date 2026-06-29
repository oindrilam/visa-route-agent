from google.adk.agents.llm_agent import Agent
from app.tools.scoring_tool import estimate_visa_route


def get_project_status() -> dict:
    """Returns current VisaRoute Agent MVP status."""
    return {
        "status": "success",
        "project": "VisaRoute Agent",
        "mvp_scope": "Indian passport holders applying for tourist, student, or business visas",
        "next_build_step": "Add visa rules and document checklist logic"
    }


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="visa_route_agent",
    description="A visa route optimizer for Indian passport holders.",
    instruction="""
You are VisaRoute Agent.

You help Indian passport holders estimate the best visa application route.

You compare:
- self-application
- assisted visa platform
- corporate travel desk
- expert visa support

Use the estimate_visa_route tool when the user gives visa purpose, destination,
role/profile, travel urgency, previous refusal status, confidence, budget sensitivity,
and corporate support availability.

Always say this is planning guidance, not official visa advice.
""",
    tools=[get_project_status, estimate_visa_route],
)
