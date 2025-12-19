import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="SHL GenAI Assessment Recommender")

st.title("🧠 SHL GenAI Assessment Recommender")

query = st.text_area(
    "Job requirement / query",
    placeholder="e.g. Need a Java developer who collaborates well with stakeholders",
    height=120
)

top_k = st.slider("Number of recommendations", 3, 10, 5)

if st.button("🔍 Recommend"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        response = requests.post(API_URL, json={
            "query": query,
            "top_k": top_k
        })

        if response.status_code != 200:
            st.error("API error")
        else:
            results = response.json()["recommended_assessments"]

            for i, item in enumerate(results, 1):
                st.markdown(f"### {i}. {item['name']}")
                st.markdown(f"- **URL:** [{item['url']}]({item['url']})")
                st.markdown(f"- **Test Type:** {', '.join(item['test_type'])}")
                st.markdown(f"- **Remote Support:** {item['remote_support']}")
                st.markdown(f"- **Adaptive Support:** {item['adaptive_support']}")
                st.markdown(f"- **Description:** {item['description']}")
                st.markdown(f"- **Duration:** {item['duration']} minutes")
                st.markdown("---")
