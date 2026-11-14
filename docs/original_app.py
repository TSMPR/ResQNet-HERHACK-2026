import streamlit as st
import pandas as pd
import pydeck as pdk
from response_engine import classify_report, get_response_guidance, summarize_incidents

st.set_page_config(page_title="ResQNet | HERHACK 2026", page_icon="🚨", layout="wide")
st.title("🚨 ResQNet")
st.subheader("AI-assisted emergency report triage and resource coordination")
st.caption("HERHACK 2026 · AI Track · Prototype")

st.error("DEMO ONLY — This is not an emergency service. It does not contact responders, dispatch help, or provide verified live resource availability. For immediate danger, contact local emergency services (112 in India) or a trusted person.")

@st.cache_data
def load_data():
    return pd.read_csv("data/sample_incidents.csv")

df = load_data()
tab1, tab2, tab3 = st.tabs(["Incident triage", "Situation dashboard", "System & limitations"])

with tab1:
    st.markdown("### Submit a sample incident report")
    report = st.text_area("Describe what happened", placeholder="Example: A road accident has blocked the main road and one person appears injured.", height=120)
    location = st.selectbox("Demo area", sorted(df["area"].unique()))
    if st.button("Assess report", type="primary"):
        if not report.strip():
            st.warning("Enter a report to assess.")
        else:
            result = classify_report(report)
            st.metric("Suggested category", result["category"])
            st.metric("Suggested priority", result["priority"])
            st.write("**Why this was suggested**")
            st.write(result["explanation"])
            st.write("**Recommended coordination checklist**")
            for item in get_response_guidance(result):
                st.write(f"- {item}")
            st.caption("A human operator must verify every report and decide what action, if any, is appropriate. Model output can be wrong.")

with tab2:
    st.markdown("### Synthetic incident overview")
    summary = summarize_incidents(df)
    a, b, c = st.columns(3)
    a.metric("Demo reports", len(df))
    b.metric("Areas represented", df["area"].nunique())
    c.metric("Categories", df["category"].nunique())
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.markdown("### Illustrative incident locations")
    map_df = df.groupby("area", as_index=False).agg(
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        reports=("incident_id", "count")
    )
    layer = pdk.Layer("ScatterplotLayer", data=map_df,
                      get_position="[longitude, latitude]",
                      get_radius="reports * 120 + 100",
                      get_fill_color=[230, 90, 60, 160],
                      pickable=True)
    view = pdk.ViewState(latitude=17.385, longitude=78.4867, zoom=10, pitch=0)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view,
                             tooltip={"text": "{area}: {reports} synthetic reports"}))
    st.caption("All incident records and coordinates are fictional examples. They are not live incidents or actual resource locations.")

with tab3:
    st.markdown("""
### How ResQNet works
1. A report is entered as text.
2. A baseline NLP classifier predicts an incident category.
3. A transparent rule layer suggests a priority for human review.
4. The app displays a coordination checklist and synthetic area-level overview.

### Responsible-use safeguards
- No emergency calls or dispatch are performed.
- No personal details should be entered into this demo.
- Reports and coordinates in the bundled dataset are synthetic.
- A model prediction is not a verified incident.
- A human responder must verify information and make decisions.
- Do not interpret an empty map or low report count as proof that an area is safe.

### Future hackathon improvements
- Replace synthetic examples with legally reusable, verified open datasets.
- Evaluate the classifier on a labelled, representative dataset.
- Add multilingual text handling and calibrated uncertainty.
- Add source timestamps, duplicate detection and human review.
- Integrate verified resource directories only after confirming availability and permissions.
""")
