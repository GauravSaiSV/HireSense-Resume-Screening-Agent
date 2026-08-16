from src.models import CandidateProfile, Experience, JobProfile
from src.matching.experience_matcher import (
    calculate_experience_years,
    match_experience,
)


def test_calculate_experience_years():
    candidate = CandidateProfile(
        name="Test Candidate",
        experience=[
            Experience(
                title="ML Engineer",
                company="Company A",
                start_date="2022",
                end_date="2024",
                description="Built ML models.",
            ),
        ],
    )

    result = calculate_experience_years(candidate)

    assert result == 2.0


def test_experience_requirement_met():
    candidate = CandidateProfile(
        name="Test Candidate",
        experience=[
            Experience(
                title="ML Engineer",
                start_date="2022",
                end_date="2025",
                description="Built machine learning models.",
            ),
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer",
        minimum_experience_years=2,
    )

    result = match_experience(candidate, job)

    assert result["candidate_years"] == 3.0
    assert result["required_years"] == 2
    assert result["met"] is True
    assert result["score"] == 1.0


def test_experience_requirement_not_met():
    candidate = CandidateProfile(
        name="Test Candidate",
        experience=[
            Experience(
                title="ML Intern",
                start_date="2024",
                end_date="2025",
                description="Worked on machine learning projects.",
            ),
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer",
        minimum_experience_years=2,
    )

    result = match_experience(candidate, job)

    assert result["candidate_years"] == 1.0
    assert result["required_years"] == 2
    assert result["met"] is False
    assert result["score"] == 0.5


def test_no_experience_requirement():
    candidate = CandidateProfile(
        name="Test Candidate",
    )

    job = JobProfile(
        job_title="AI/ML Engineer",
        minimum_experience_years=None,
    )

    result = match_experience(candidate, job)

    assert result["met"] is True
    assert result["score"] == 1.0

def test_present_end_date():
    candidate = CandidateProfile(
        name="Test Candidate",
        experience=[
            Experience(
                title="ML Engineer",
                start_date="Jan 2024",
                end_date="Present",
                description="Built machine learning systems.",
            ),
        ],
    )

    result = calculate_experience_years(candidate)

    assert result is not None
    assert result >= 2.5


def test_month_level_dates():
    candidate = CandidateProfile(
        name="Test Candidate",
        experience=[
            Experience(
                title="ML Engineer",
                start_date="Jan 2022",
                end_date="Jun 2024",
                description="Built machine learning systems.",
            ),
        ],
    )

    result = calculate_experience_years(candidate)

    assert result == 2.4