from src.matching.normalizer import (
    canonicalize_skill,
    canonicalize_skills,
    normalize_skill,
    normalize_skills,
)


def test_normalize_skill():
    assert normalize_skill("Python") == "python"
    assert normalize_skill(" ML ") == "machine learning"
    assert normalize_skill("SKLEARN") == "scikit-learn"
    assert normalize_skill("Postgres") == "postgresql"


def test_normalize_skills():
    skills = [
        "Python",
        "python",
        "ML",
        "Machine Learning",
        "SQL",
    ]

    result = normalize_skills(skills)

    assert result == [
        "python",
        "machine learning",
        "sql",
    ]


def test_canonicalize_skill_phrase():
    result = canonicalize_skill(
        "Machine Learning concepts and algorithms"
    )

    assert result == [
        "machine learning"
    ]


def test_canonicalize_multiple_skills():
    result = canonicalize_skill(
        "cloud platforms such as AWS or Google Cloud"
    )

    assert set(result) == {
        "aws",
        "google cloud",
    }


def test_canonicalize_skills():
    skills = [
        "Python",
        "Machine Learning concepts and algorithms",
        "ML",
        "TensorFlow",
    ]

    result = canonicalize_skills(skills)

    assert result == [
        "python",
        "machine learning",
        "tensorflow",
    ]