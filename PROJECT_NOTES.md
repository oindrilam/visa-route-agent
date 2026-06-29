# VisaRoute Agent - Project Notes

## Problem
Visa applicants do not know whether they should self-apply or use assisted visa services. They also underestimate calendar days, active effort hours, document gaps, interview/biometrics, and risk.

## Target User
Indian passport holders applying for tourist, student, or business visas.

## Solution
VisaRoute Agent compares visa routes using:
- calendar days
- active effort hours
- mandatory personal presence
- document readiness
- assisted-service worth-it score

## Core Logic
calendar_days = document_prep_days + appointment_wait_days + processing_days + buffer_days

active_effort_hours = form_hours + document_hours + appointment_hours + travel_hours + interview_hours + followup_hours

assisted_worth_it_score = urgency + complexity + time_value + appointment_difficulty + refusal_risk - self_confidence - budget_sensitivity

## Course Concepts To Show
- ADK multi-agent system
- MCP/tool usage
- Agents CLI demo
- Security guardrails
- Deployability / reproducible setup

## Screenshots To Capture Later
- Folder structure
- CLI running
- Agent response
- Architecture diagram
- Sample recommendation
- Antigravity/Cursor coding screen
