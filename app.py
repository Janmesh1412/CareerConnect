"""Streamlit demo for explainable resume-to-job matching."""
import streamlit as st
from src.career_matcher import match_resume_to_jobs

st.set_page_config(page_title="CareerConnect | AI Job Matcher", page_icon="🎯", layout="wide")
st.title("🎯 CareerConnect — AI Job Matcher")
st.caption("A transparent resume-to-role matching demo. Your text is processed in this app session and is not uploaded to a third-party AI service.")

SAMPLE_JOBS = [
    {"title": "Junior Python Developer", "company": "DemoTech", "description": "Build Python APIs with FastAPI, SQL databases, Git, Docker, unit testing and cloud deployment."},
    {"title": "Machine Learning Engineer", "company": "DataWorks", "description": "Develop machine learning pipelines using Python, pandas, scikit-learn, feature engineering, model evaluation and NLP."},
    {"title": "Generative AI Engineer", "company": "Nova Labs", "description": "Build LLM applications with retrieval augmented generation, embeddings, vector databases, prompt engineering and evaluation."},
    {"title": "Industrial Data Engineer", "company": "PlantOps", "description": "Integrate industrial time-series data, Python, SQL, dashboards, anomaly detection, predictive maintenance and PI historians."},
]

with st.sidebar:
    st.header("Job catalogue")
    st.write(f"{len(SAMPLE_JOBS)} illustrative roles loaded")
    st.caption("Demo descriptions only; replace these with verified live job descriptions before applying.")
    top_k = st.slider("Number of matches", min_value=1, max_value=len(SAMPLE_JOBS), value=4)

resume = st.text_area("Paste your resume text or skills", height=260, placeholder="Example: Python, pandas, SQL, machine learning, scikit-learn, Streamlit, FastAPI...")
if st.button("Find matching roles", type="primary", use_container_width=True):
    if not resume.strip():
        st.warning("Add resume text or skills to get started.")
    else:
        matches = match_resume_to_jobs(resume, SAMPLE_JOBS, top_k=top_k)
        st.subheader("Your strongest matches")
        for item in matches:
            with st.container(border=True):
                left, right = st.columns([4, 1])
                left.markdown(f"**{item['title']}** · {item['company']}")
                right.metric("Text match", f"{item['score']}%")
                st.progress(min(int(item["score"]), 100))
                st.markdown("**Overlapping terms**")
                st.write(", ".join(item["matched_skills"]) or "No direct overlap found")
                st.markdown("**Terms to explore**")
                st.write(", ".join(item["missing_skills"]) or "No additional terms identified")
        st.info("Scores measure keyword-based text similarity, not candidate quality, interview probability, or hiring decisions. Review every role manually.")

st.divider()
st.caption("Privacy note: this starter app does not save resumes. Avoid entering sensitive personal identifiers in demo environments.")
