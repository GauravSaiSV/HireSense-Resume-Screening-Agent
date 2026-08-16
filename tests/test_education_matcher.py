from src.models import CandidateProfile, Education, JobProfile

from src.matching.education_matcher import (
    education_match_score,
    match_education,
)


def test_btech_computer_science_matches():
    score = education_match_score(
        "B.Tech in Computer Science and Artificial Intelligence",
        "B.Tech in Computer Science",
    )

    assert score == 1.0


def test_btech_alias_matches():
    score = education_match_score(
        "BTech Computer Science",
        "Bachelor of Technology in Computer Science",
    )

    assert score == 1.0


def test_unrelated_degree_does_not_match():
    score = education_match_score(
        "B.Com in Commerce",
        "B.Tech in Computer Science",
    )

    assert score == 0.0


def test_matching_job_education_requirements():
    candidate = CandidateProfile(
        name="Test Candidate",
        education=[
            Education(
                degree="B.Tech in Computer Science and Artificial Intelligence",
                institution="Test University",
                year="2026",
            )
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        education_requirements=[
            "B.Tech or equivalent in Computer Science",
        ],
    )

    result = match_education(
        candidate,
        job,
    )

    assert result["matched"] == [
        "B.Tech or equivalent in Computer Science"
    ]

    assert result["missing"] == []

    assert result["score"] == 1.0

    assert result["met"] is True


def test_missing_education_requirement():
    candidate = CandidateProfile(
        name="Test Candidate",
        education=[
            Education(
                degree="B.Com in Commerce",
                institution="Test University",
                year="2026",
            )
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        education_requirements=[
            "B.Tech in Computer Science",
        ],
    )

    result = match_education(
        candidate,
        job,
    )

    assert result["matched"] == []

    assert result["missing"] == [
        "B.Tech in Computer Science"
    ]

    assert result["score"] == 0.0

    assert result["met"] is False


def test_no_education_requirement():
    candidate = CandidateProfile(
        name="Test Candidate",
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        education_requirements=[],
    )

    result = match_education(
        candidate,
        job,
    )

    assert result["score"] == 1.0
    assert result["met"] is True