import unittest
from src.career_matcher import match_resume_to_jobs, tokenize


class CareerMatcherTests(unittest.TestCase):
    def setUp(self):
        self.jobs = [
            {"title": "Python Engineer", "company": "A", "description": "Python APIs SQL testing"},
            {"title": "Designer", "company": "B", "description": "Figma typography visual design"},
        ]

    def test_relevant_job_ranks_first(self):
        results = match_resume_to_jobs("Python API development and SQL", self.jobs)
        self.assertEqual(results[0]["title"], "Python Engineer")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_empty_resume_rejected(self):
        with self.assertRaises(ValueError):
            match_resume_to_jobs("   ", self.jobs)

    def test_invalid_top_k_rejected(self):
        with self.assertRaises(ValueError):
            match_resume_to_jobs("Python", self.jobs, top_k=0)

    def test_invalid_job_rejected(self):
        with self.assertRaises(ValueError):
            match_resume_to_jobs("Python", [{"title": "Missing description"}])

    def test_empty_job_list(self):
        self.assertEqual(match_resume_to_jobs("Python developer", []), [])

    def test_tokenization_normalizes_case(self):
        self.assertEqual(tokenize("Python PYTHON SQL"), ["python", "python", "sql"])


if __name__ == "__main__":
    unittest.main()
