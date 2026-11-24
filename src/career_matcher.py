"""Explainable, dependency-light resume-to-job matching utilities."""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z+#.]{1,}")
STOP_WORDS = {
    "and", "the", "for", "with", "from", "you", "your", "are", "our", "this",
    "that", "will", "have", "has", "into", "their", "they", "them", "who", "what",
    "when", "where", "how", "can", "must", "should", "able", "using", "used",
    "years", "year", "work", "team", "role", "job", "experience", "strong", "good",
}


def tokenize(text: str) -> list[str]:
    """Normalize text into useful lowercase tokens."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOP_WORDS]


def _tfidf_vectors(documents: list[list[str]]) -> list[dict[str, float]]:
    if not documents:
        return []
    document_frequency: Counter[str] = Counter()
    for tokens in documents:
        document_frequency.update(set(tokens))
    total = len(documents)
    vectors: list[dict[str, float]] = []
    for tokens in documents:
        counts = Counter(tokens)
        length = len(tokens)
        if not length:
            vectors.append({})
            continue
        vectors.append({
            term: (count / length) * (math.log((1 + total) / (1 + document_frequency[term])) + 1)
            for term, count in counts.items()
        })
    return vectors


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(value * right.get(term, 0.0) for term, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def match_resume_to_jobs(resume: str, jobs: Iterable[dict[str, str]], top_k: int = 5) -> list[dict[str, object]]:
    """Rank jobs against resume text and return similarity and term overlap.

    Each job must contain non-empty title and description strings.
    Scores are lexical similarity, not a hiring probability.
    """
    if not isinstance(resume, str) or not resume.strip():
        raise ValueError("resume must not be empty")
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be a positive integer")

    job_list = list(jobs)
    for index, job in enumerate(job_list):
        if not isinstance(job, dict) or not str(job.get("title", "")).strip() or not str(job.get("description", "")).strip():
            raise ValueError(f"job at index {index} must include title and description")

    token_docs = [tokenize(resume)] + [tokenize(f"{job['title']} {job['description']}") for job in job_list]
    vectors = _tfidf_vectors(token_docs)
    resume_terms = set(token_docs[0])
    results: list[dict[str, object]] = []
    for job, tokens, vector in zip(job_list, token_docs[1:], vectors[1:]):
        job_terms = set(tokens)
        matched = sorted(resume_terms & job_terms)
        missing = sorted(job_terms - resume_terms)
        score = round(_cosine(vectors[0], vector) * 100, 1)
        results.append({
            "title": str(job["title"]).strip(),
            "company": str(job.get("company", "Not specified")).strip() or "Not specified",
            "score": score,
            "matched_skills": matched[:12],
            "missing_skills": missing[:12],
            "match_summary": f"{len(matched)} overlapping terms; review missing terms for learning opportunities.",
        })
    return sorted(results, key=lambda item: (-float(item["score"]), str(item["title"]).lower()))[:top_k]
