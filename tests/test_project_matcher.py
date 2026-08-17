from src.models import CandidateProfile, JobProfile

from src.matching.project_matcher import (
    match_projects,
    normalize_text,
    project_relevance_score,
)


def test_normalize_project_text():
    result = normalize_text(
        "Built an AI/ML model using Python!"
    )

    assert result == (
        "built an ai ml model using python"
    )


def test_relevant_project_gets_high_score():
    project = (
        "Built an image classification system "
        "using Python, TensorFlow and deep learning."
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning",
        ],
        preferred_skills=[
            "TensorFlow",
            "Deep Learning",
        ],
        keywords=[
            "image classification",
            "deep learning",
        ],
        responsibilities=[
            "Develop and evaluate machine learning models.",
        ],
    )

    score = project_relevance_score(
        project,
        job,
    )

    assert score > 0.3


def test_unrelated_project_gets_low_score():
    project = (
        "Built a responsive e-commerce website "
        "using HTML, CSS and JavaScript."
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning",
        ],
        preferred_skills=[
            "TensorFlow",
            "PyTorch",
        ],
        keywords=[
            "machine learning",
            "deep learning",
        ],
        responsibilities=[
            "Develop and evaluate machine learning models.",
        ],
    )

    score = project_relevance_score(
        project,
        job,
    )

    assert score < 0.2


def test_match_projects():
    candidate = CandidateProfile(
        name="Test Candidate",
        projects=[
            (
                "Built an image classification system "
                "using Python and TensorFlow."
            ),
            (
                "Built a simple portfolio website "
                "using HTML and CSS."
            ),
        ],
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning",
        ],
        preferred_skills=[
            "TensorFlow",
        ],
        keywords=[
            "image classification",
            "machine learning",
        ],
        responsibilities=[
            "Develop machine learning models.",
        ],
    )

    result = match_projects(
        candidate,
        job,
    )

    assert len(result["projects"]) == 2

    assert result["best_score"] >= (
        result["average_score"]
    )

    assert result["projects"][0]["score"] > (
        result["projects"][1]["score"]
    )

def test_deep_learning_project_matches_machine_learning_requirement():
    project = (
        "Built an image classification system "
        "using deep learning."
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Machine Learning",
        ],
    )

    score = project_relevance_score(
        project,
        job,
    )

    assert score > 0.0


def test_image_classification_is_recognized_as_ml_project():
    project = (
        "Developed an image classification model "
        "for identifying objects."
    )

    job = JobProfile(
        job_title="Machine Learning Engineer",
        required_skills=[
            "Machine Learning",
        ],
    )

    score = project_relevance_score(
        project,
        job,
    )

    assert score > 0.0

def test_full_project_description_gets_strong_relevance_score():
    project = (
        "Image Classification System - "
        "Built an image classification system using "
        "Python, TensorFlow and deep learning."
    )

    job = JobProfile(
        job_title="AI/ML Engineer Intern",
        required_skills=[
            "Python",
            "Machine Learning",
        ],
        preferred_skills=[
            "TensorFlow",
            "Deep Learning",
        ],
        keywords=[
            "image classification",
            "deep learning",
        ],
        responsibilities=[
            "Develop and evaluate machine learning models.",
        ],
    )

    score = project_relevance_score(
        project,
        job,
    )

    assert score >= 0.7