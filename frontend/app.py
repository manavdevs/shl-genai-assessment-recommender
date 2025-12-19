import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="SHL GenAI Assessment Recommender",
    layout="centered"
)

st.title("🧠 SHL GenAI Assessment Recommender")

st.markdown(
    """
    Enter a job description or hiring requirement and get recommended SHL assessments.
    """
)

query = st.text_area(
    "Job requirement / query",
    placeholder="e.g. Need a Java developer who collaborates well with stakeholders",
    height=120
)

top_k = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

if st.button("🔍 Recommend"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding best assessments..."):
            payload = {
                "query": query,
                "top_k": top_k
            }

            try:
                response = requests.post(API_URL, json=payload, timeout=60)

                if response.status_code != 200:
                    st.error("API error. Please check backend logs.")
                else:
                    results = response.json()["results"]

                    st.subheader("✅ Recommended Assessments")

                    for i, item in enumerate(results, 1):
                        st.markdown(f"### {i}. {item['name']}")
                        st.markdown(f"- **URL:** [{item['url']}]({item['url']})")
                        st.markdown("---")

            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")
