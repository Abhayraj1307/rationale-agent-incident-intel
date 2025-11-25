import streamlit as st

from app.ingest import load_incident_docs
from app.claims import extract_claims
from app.rationale import aggregate_claims, compute_confidence, format_rationale_text


@st.cache_resource
def load_data():
    docs = load_incident_docs()
    by_id = {d["incident_id"]: d for d in docs}
    return by_id


def main():
    st.set_page_config(
        page_title="Rationale Agent – Incident Intelligence",
        layout="wide"
    )
    st.title("Rationale Agent – Incident Intelligence (Demo)")

    incidents = load_data()
    if not incidents:
        st.error("No incident documents found in data/incidents.")
        return

    incident_ids = sorted(incidents.keys())
    selected_id = st.selectbox("Select an incident to analyze:", incident_ids)

    if not selected_id:
        return

    incident = incidents[selected_id]

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Incident Document")
        st.caption(f"Source file: `{incident['filename']}`")
        st.text_area(
            "Raw text",
            incident["text"],
            height=400,
        )

    with col_right:
        st.subheader("Analysis")

        if st.button("Run Rationale Analysis"):
            claims = extract_claims(
                incident_id=incident["incident_id"],
                filename=incident["filename"],
                text=incident["text"],
            )

            if not claims:
                st.error("No claims extracted from this incident.")
                return

            agg = aggregate_claims(claims)
            confidence = compute_confidence(agg["support_counts"])
            rationale_text = format_rationale_text(incident["incident_id"], agg)

            st.markdown("### Decision Summary")
            st.markdown(rationale_text)
            st.markdown(f"**Confidence (heuristic):** `{confidence}`")

            st.markdown("### Evidence by Cause Category")
            for cause, cause_claims in agg["by_cause"].items():
                if not cause_claims:
                    continue
                st.markdown(f"#### {cause} ({len(cause_claims)} claim(s))")
                for c in cause_claims:
                    st.markdown(f"- **Summary:** {c['summary']}")
                    st.caption(
                        f"Impact: `{c['impact_scope']}` | System: `{c['system']}`  \n"
                        f"Evidence: {c['evidence_snippet'][:280]}..."
                    )
        else:
            st.info("Click **Run Rationale Analysis** to extract claims and build a rationale.")


if __name__ == "__main__":
    main()
