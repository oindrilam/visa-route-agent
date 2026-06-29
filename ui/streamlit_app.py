import os
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


st.set_page_config(page_title="VisaRoute Agent", page_icon="??", layout="wide")

st.title("VisaRoute Agent")
st.write("A neutral visa route optimizer for Indian passport holders.")
st.caption("Planning guidance only. Not official visa advice.")

with st.form("visa_form"):
    destination_country = st.selectbox("Destination country", ["Germany", "UK", "UAE"])
    visa_purpose = st.selectbox("Visa purpose", ["tourist", "business", "student"])
    user_segment = st.text_input("Your profile / role", "VP")
    travel_days_from_now = st.number_input("Travel starts in how many days?", min_value=1, max_value=365, value=20)
    previous_refusal = st.checkbox("Previous visa refusal?")
    self_confidence = st.slider("Self-application confidence", 1, 10, 4)
    budget_sensitivity = st.slider("Budget sensitivity", 1, 10, 2)
    corporate_support_available = st.checkbox("Corporate support available?")

    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    query_text = f"{visa_purpose} visa for {destination_country}"

    guardrail_response = requests.post(
        f"{BACKEND_URL}/guardrail",
        json={"user_query": query_text},
        timeout=10
    ).json()

    if not guardrail_response["allowed"]:
        st.error(guardrail_response["message"])
    else:
        recommendation = requests.post(
            f"{BACKEND_URL}/recommend",
            json={
                "visa_purpose": visa_purpose,
                "destination_country": destination_country,
                "user_segment": user_segment,
                "travel_days_from_now": travel_days_from_now,
                "previous_refusal": previous_refusal,
                "self_confidence": self_confidence,
                "budget_sensitivity": budget_sensitivity,
                "corporate_support_available": corporate_support_available,
            },
            timeout=10
        ).json()

        checklist = requests.post(
            f"{BACKEND_URL}/checklist",
            json={
                "visa_purpose": visa_purpose,
                "destination_country": destination_country,
                "previous_refusal": previous_refusal,
            },
            timeout=10
        ).json()

        st.subheader("Recommendation")
        st.success(recommendation["recommendation"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated calendar days", recommendation["estimated_calendar_days"])
        col2.metric("Self-apply effort hours", recommendation["self_apply_effort_hours"])
        col3.metric("Assisted worth-it score", f"{recommendation['assisted_worth_it_score']}/100")

        st.subheader("Visa process signals")
        st.write(f"**Visa category:** {checklist['visa_category']}")
        st.write(f"**Appointment required:** {checklist['appointment_required']}")
        st.write(f"**Biometrics required:** {checklist['biometrics_required']}")
        st.write(f"**Interview:** {checklist['interview_requirement']}")

        st.subheader("Document checklist")
        for document in checklist["document_checklist"]:
            st.checkbox(document, value=False)

        st.info(recommendation["note"])
