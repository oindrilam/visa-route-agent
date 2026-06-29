from google.adk.agents.llm_agent import Agent


def get_project_status() -> dict:
    """Returns current VisaRoute Agent MVP status."""
    return {
        "status": "success",
        "project": "VisaRoute Agent",
        "mvp_scope": "Indian passport holders applying for tourist, student, or business visas",
        "next_build_step": "Add visa route business logic tools"
    }


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="visa_route_agent",
    description="A visa route optimizer for Indian passport holders.",
    instruction="""
You are VisaRoute Agent.
Help users compare self-application, assisted platforms, corporate travel desk, and expert help.
For now, explain that the project skeleton is ready and use the get_project_status tool when asked about project status.
""",
    tools=[get_project_status],
)
