import pytest

from src.models import (
    CandidateProfile,
    Education,
    Experience,
    JobProfile,
)

from src.scoring.scorer import (
    WEIGHTS,
    calculate_weighted_score,
    score_candidate,
)


def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == 1.0


def test_perfect_score():
    score = calculate_weighted_score(
        required_skills_score=1.0,
        preferred_skills_score=1.0,
        experience_score=1.0,
        education_score=1.0,
        project_score=1.0,
    )

    assert score == 100.0


def test_zero_score():
    score = calculate_weighted_score(
        required_skills_score=0.0,
        preferred_skills_score=0.0,
        experience_score=0.0,
        education_score=0.0,
        project_score=0.0,
    )

    assert score == 0.0


def test_partial_weighted_score():
    score = calculate_weighted_score(
        required_skills_score=0.75,
        preferred_skills_score=0.50,
        experience_score=1.0,
        education_score=1.0,
        project_score=0.50,
    )

    assert score == 75.0


def test_invalid_score_above_one():
    with pytest.raises(ValueError):
        calculate_weighted_score(
            required_skills_score=1.1,
            preferred_skills_score=0.5,
            experience_score=1.0,
            education_score=1.0,
            project_score=0.5,
        )


def test_invalid_score_below_zero():
    with pytest.raises(ValueError):
        calculate_weighted_score(
            required_skills_score=0.5,
            preferred_skills_score=-0.1,
            experience_score=1.0,
            education_score=1.0,
            project_score=0.5,
        )


def test_score_candidate():
    candidate = CandidateProfile(
        name="Test Candidate",

        skills=[
            "Python",
            "ML",
            "SQL",
            "TensorFlow",
        ],

        education=[
            Education(
                degree=(
                    "B.Tech in Computer Science "
                    "and Artificial Intelligence"
                ),
                institution="Test University",
                year="2026",
            )
        ],

        experience=[
            Experience(
                title="ML Engineer",
                company="Test Company",
                start_date="2022",
                end_date="2025",
                description="Built machine learning models.",
            )
        ],

        projects=[
            (
                "Built an image classification system "
                "using Python and TensorFlow."
            )
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",

        required_skills=[
            "Python",
            "Machine Learning",
            "SQL",
        ],

        preferred_skills=[
            "TensorFlow",
            "PyTorch",
        ],

        minimum_experience_years=2,

        education_requirements=[
            "B.Tech in Computer Science",
        ],

        responsibilities=[
            "Develop machine learning models.",
        ],

        keywords=[
            "machine learning",
            "image classification",
        ],
    )

    result = score_candidate(
        candidate,
        job,
    )

    assert result["candidate_name"] == "Test Candidate"

    assert 0 <= result["final_score"] <= 100

    assert result["final_score"] > 70

    assert "breakdown" in result

    assert "details" in result

    assert set(result["breakdown"]) == {
        "required_skills",
        "preferred_skills",
        "experience",
        "education",
        "projects",
    }