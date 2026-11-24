# CareerConnect — Explainable AI Job Matcher

A portfolio project that ranks job descriptions against resume text using TF-IDF and cosine similarity. It includes a Streamlit interface, transparent overlap/gap terms, and unit tests.

**Important:** The score is lexical similarity, not a probability of getting hired or a measure of candidate worth. Included roles are illustrative examples, not live vacancies.

## Features
- Resume/skills text input with no external AI API call
- TF-IDF and cosine-similarity ranking in a readable Python module
- Matched and missing terms for explainability
- Configurable number of recommendations
- Input validation and six standard-library unit tests
- No resume persistence in this starter implementation

## Quick start
1. Create and activate a virtual environment: python -m venv .venv
2. Install dependencies: pip install -r requirements.txt
3. Launch the app: streamlit run app.py

## Run tests
python -m unittest discover -s tests -v

## How matching works
1. Normalize resume and job descriptions into tokens.
2. Build TF-IDF vectors over the resume and supplied job catalogue.
3. Compute cosine similarity and sort by descending score.
4. Display overlapping and role-only terms as explainability hints.

This is a lightweight baseline, not a semantic embedding model. Future iterations could add vetted job-feed ingestion, multilingual embeddings, user-controlled skill taxonomies, evaluation against labelled examples, and bias/privacy reviews. Do not use automated scores as the sole basis for employment decisions.

## Customizing the catalogue
Edit SAMPLE_JOBS in app.py and provide verified, current job descriptions. Do not represent sample roles as active openings unless checked against the employer's official listing.

## Tech stack
Python · Streamlit · TF-IDF · Cosine Similarity · unittest

## License
MIT — see LICENSE.
