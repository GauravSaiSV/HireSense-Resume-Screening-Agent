from src.models import CandidateProfile, JobProfile
from src.matching.skill_matcher import match_skills


def test_required_and_preferred_skill_matching():
    candidate = CandidateProfile(
        name="Test Candidate",
        skills=[
            "Python",
            "ML",
            "SQL",
            "TensorFlow",
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning",
            "SQL",
            "Git",
        ],
        preferred_skills=[
            "TensorFlow",
            "PyTorch",
            "AWS",
        ],
    )

    result = match_skills(candidate, job)

    assert result["required"]["matched"] == [
        "python",
        "machine learning",
        "sql",
    ]

    assert result["required"]["missing"] == [
        "git",
    ]

    assert result["preferred"]["matched"] == [
        "tensorflow",
    ]

    assert result["preferred"]["missing"] == [
        "pytorch",
        "aws",
    ]

    assert result["required"]["score"] == 0.75
    assert result["preferred"]["score"] == 1 / 3

def test_matching_handles_messy_skill_phrases():
    candidate = CandidateProfile(
        name="Test Candidate",
        skills=[
            "Python",
            "ML",
            "SQL",
            "AWS",
            "Google Cloud",
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning concepts and algorithms",
            "SQL",
        ],
        preferred_skills=[
            "cloud platforms such as AWS or Google Cloud",
            "TensorFlow",
        ],
    )

    result = match_skills(candidate, job)

    assert set(result["required"]["matched"]) == {
        "python",
        "machine learning",
        "sql",
    }

    assert result["required"]["missing"] == []

    assert set(result["preferred"]["matched"]) == {
        "aws",
        "google cloud",
    }

    assert result["preferred"]["missing"] == [
        "tensorflow",
    ]

    assert result["required"]["score"] == 1.0