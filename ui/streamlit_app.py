import os
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


st.set_page_config(page_title="VisaRoute Agent", page_icon="🛂", layout="wide")

st.title("VisaRoute Agent")
st.write(
    "A neutral visa route optimizer using passport, source country, destination, "
    "purpose, profile, and risk signals."
)
st.caption("Planning guidance only. Not official visa advice.")


with st.container():
    country_options = [
        "India",
        "United Kingdom",
        "United States",
        "Canada",
        "Japan",
        "Germany",
        "France",
        "Italy",
        "Spain",
        "Netherlands",
        "Switzerland",
        "Ireland",
        "Ukraine"
    ]

    passport_country = st.selectbox("Passport / nationality", country_options, index=0)
    source_country = st.selectbox("Applying from / source country", country_options, index=0)
    destination_country = st.selectbox("Destination country", country_options, index=5)

    visa_purpose = st.selectbox(
        "Visa purpose",
        ["tourist", "business", "student", "work", "dependent_family", "transit"]
    )

    user_segment = st.selectbox(
        "Your profile / role",
        [
            "general",
            "student",
            "employee",
            "senior employee",
            "VP",
            "CXO",
            "business owner",
            "homemaker",
            "minor",
            "spouse",
            "child",
            "parent"
        ]
    )

    dependent_type = st.selectbox(
        "Dependent / family type",
        [
            "not_applicable",
            "spouse",
            "child",
            "parent",
            "family_visitor",
            "dependent_of_student",
            "dependent_of_worker"
        ],
        disabled=(visa_purpose != "dependent_family")
    )

    if visa_purpose != "dependent_family":
        st.caption("Dependent / family type: Not applicable for selected visa purpose.")

    travel_days_from_now = st.number_input(
        "Travel starts in how many days?",
        min_value=1,
        max_value=365,
        value=20
    )

    previous_refusal = st.checkbox("Previous visa refusal?")
    self_confidence = st.slider("Self-application confidence", 1, 10, 4)
    budget_sensitivity = st.slider("Budget sensitivity", 1, 10, 2)

    corporate_support_applicable = visa_purpose in ["business", "work"]

    if corporate_support_applicable:
        corporate_support_available = st.checkbox(
            "Corporate support available?",
            key=f"corporate_support_enabled_{visa_purpose}"
        )
    else:
        corporate_support_available = False
        st.checkbox(
            "Corporate support available?",
            value=False,
            disabled=True,
            key=f"corporate_support_disabled_{visa_purpose}"
        )
        st.caption("Corporate support: Not applicable for selected visa purpose.")

    submitted = st.button("Get Recommendation")


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
                "passport_country": passport_country,
                "source_country": source_country,
                "destination_country": destination_country,
                "visa_purpose": visa_purpose,
                "user_segment": user_segment,
                "dependent_type": dependent_type,
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
                "passport_country": passport_country,
                "source_country": source_country,
                "destination_country": destination_country,
                "visa_purpose": visa_purpose,
                "user_segment": user_segment,
                "dependent_type": dependent_type,
                "previous_refusal": previous_refusal,
            },
            timeout=10
        ).json()

        st.subheader("Recommendation")
        st.success(recommendation["recommendation"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated calendar days", recommendation["estimated_calendar_days"])
        col2.metric("Self-apply effort hours", recommendation["self_apply_effort_hours"])
        col3.metric(
            "Assisted worth-it score",
            f"{recommendation['assisted_worth_it_score']}/100"
        )

        st.subheader("Visa process signals")
        st.write(f"**Visa category:** {checklist['visa_category']}")
        st.write(f"**Appointment required:** {checklist['appointment_required']}")
        st.write(f"**Biometrics required:** {checklist['biometrics_required']}")
        st.write(f"**Interview:** {checklist['interview_requirement']}")

        st.subheader("Document checklist")
        for document in checklist["document_checklist"]:
            st.checkbox(document, value=False)

        st.info(recommendation["note"])

        links_response = requests.get(
            f"{BACKEND_URL}/source-links/{destination_country}",
            timeout=10
        )

        if links_response.ok:
            source_links = links_response.json()

            st.subheader("Official / Authorized Visa Sources")

            if source_links.get("available"):
                st.write(
                    f"**Primary authority:** "
                    f"{source_links.get('primary_authority', 'Not configured')}"
                )

                st.write("**Official government links:**")
                for link in source_links.get("official_links", []):
                    st.markdown(f"- [{link['label']}]({link['url']})")

                authorized_links = source_links.get("authorized_service_links", [])
                if authorized_links:
                    st.write("**Authorized service links:**")
                    for link in authorized_links:
                        st.markdown(f"- [{link['label']}]({link['url']})")

                st.caption(
                    source_links.get(
                        "disclaimer",
                        "Always verify visa rules on the official website before applying."
                    )
                )
            else:
                st.info(
                    source_links.get(
                        "message",
                        "No official source links configured yet for this destination."
                    )
                )

        safety_response = requests.post(
            f"{BACKEND_URL}/safety-assessment",
            json={
                "destination_country": destination_country,
                "visa_purpose": visa_purpose,
                "user_segment": user_segment,
            },
            timeout=10
        )

        if safety_response.ok:
            safety = safety_response.json()

            st.subheader("Destination Safety Assessment")
            st.caption(safety.get("disclaimer", ""))

            for category in safety.get("safety_categories", {}).values():
                with st.expander(category["label"]):
                    st.write(f"**Planning signal:** {category['planning_signal']}")
                    st.write(
                        f"**Last 5-year count status:** "
                        f"{category.get('last_5_year_count_status', 'source_review_required')}"
                    )
                    st.write(
                        f"**Traveler-specific count available:** "
                        f"{category.get('traveler_specific_count_available', False)}"
                    )

                    st.write("**What to check:**")
                    for item in category.get("what_to_check", []):
                        st.markdown(f"- {item}")

            profile_notes = safety.get("profile_notes", [])
            if profile_notes:
                st.write("**Profile-specific notes:**")
                for note in profile_notes:
                    st.markdown(f"- {note}")

            st.write("**Official crime data source families:**")
            for source in safety.get("official_crime_data_sources", []):
                st.markdown(
                    f"- {source['name']} "
                    f"({source['source_type']}, coverage: {source['coverage']})"
                )

            st.write("**Travel advisory source families:**")
            for source in safety.get("travel_advisory_sources", []):
                st.markdown(
                    f"- {source['name']} "
                    f"({source['source_type']})"
                )

            st.write(f"**Counting rule:** {safety.get('counting_rule', '')}")
            st.info(safety.get("source_confidence_explanation", ""))
        else:
            st.warning("Safety assessment is temporarily unavailable.")