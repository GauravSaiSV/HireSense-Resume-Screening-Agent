import re

from src.models import CandidateProfile, JobProfile


DEGREE_ALIASES = {
    "btech": "bachelor of technology",
    "b.tech": "bachelor of technology",
    "b tech": "bachelor of technology",
    "be": "bachelor of engineering",
    "b.e": "bachelor of engineering",
    "b e": "bachelor of engineering",
    "mtech": "master of technology",
    "m.tech": "master of technology",
    "m tech": "master of technology",
    "me": "master of engineering",
    "m.e": "master of engineering",
    "m e": "master of engineering",
    "bsc": "bachelor of science",
    "b.sc": "bachelor of science",
    "b sc": "bachelor of science",
    "msc": "master of science",
    "m.sc": "master of science",
    "m sc": "master of science",
    "bca": "bachelor of computer applications",
    "mca": "master of computer applications",
}


FIELD_ALIASES = {
    "cs": "computer science",
    "cse": "computer science",
    "computer science engineering": "computer science",
    "ai": "artificial intelligence",
    "aiml": "artificial intelligence machine learning",
    "ai ml": "artificial intelligence machine learning",
    "machine learning": "machine learning",
    "ml": "machine learning",
    "data science": "data science",
    "ds": "data science",
}


def normalize_education_text(text: str) -> str:
    """
    Normalize an education-related phrase for comparison.
    """

    if not text:
        return ""

    normalized = text.lower().strip()

    normalized = normalized.replace("&", " and ")

    normalized = re.sub(r"[/,-]", " ", normalized)

    normalized = re.sub(r"\s+", " ", normalized)

    # Apply degree aliases.
    for alias, canonical in DEGREE_ALIASES.items():
        pattern = rf"\b{re.escape(alias)}\b"
        normalized = re.sub(
            pattern,
            canonical,
            normalized,
        )

    # Apply field aliases.
    for alias, canonical in FIELD_ALIASES.items():
        pattern = rf"\b{re.escape(alias)}\b"
        normalized = re.sub(
            pattern,
            canonical,
            normalized,
        )

    return normalized.strip()


def extract_degree_level(text: str) -> str | None:
    """
    Identify the broad academic level from an education phrase.
    """

    normalized = normalize_education_text(text)

    degree_levels = [
        ("doctor", "doctorate"),
        ("phd", "doctorate"),
        ("doctorate", "doctorate"),
        ("master", "master"),
        ("postgraduate", "master"),
        ("bachelor", "bachelor"),
        ("undergraduate", "bachelor"),
        ("diploma", "diploma"),
    ]

    for keyword, level in degree_levels:
        if re.search(
            rf"\b{re.escape(keyword)}\b",
            normalized,
        ):
            return level

    return None


def extract_fields(text: str) -> set[str]:
    """
    Extract known academic fields from an education phrase.
    """

    normalized = normalize_education_text(text)

    fields = {
        "computer science",
        "artificial intelligence",
        "machine learning",
        "data science",
        "information technology",
        "electronics",
        "electrical engineering",
        "mechanical engineering",
        "civil engineering",
        "commerce",
        "business administration",
        "mathematics",
        "physics",
    }

    return {
        field
        for field in fields
        if field in normalized
    }


def education_match_score(
    candidate_degree: str,
    required_education: str,
) -> float:
    """
    Calculate a deterministic education compatibility score.

    1.0 = strong match
    0.5 = partial/related match
    0.0 = no meaningful match
    """

    candidate = normalize_education_text(
        candidate_degree
    )

    required = normalize_education_text(
        required_education
    )

    if not candidate or not required:
        return 0.0

    candidate_level = extract_degree_level(candidate)
    required_level = extract_degree_level(required)

    candidate_fields = extract_fields(candidate)
    required_fields = extract_fields(required)

    # If both sides specify degree levels and they differ,
    # treat them as incompatible.
    if (
        candidate_level
        and required_level
        and candidate_level != required_level
    ):
        return 0.0

    # If the requirement specifies fields, compare them.
    if required_fields:

        if not candidate_fields:
            return 0.0

        overlap = (
            candidate_fields & required_fields
        )

        if not overlap:
            return 0.0

        # Candidate contains at least one required field.
        if overlap == required_fields:
            return 1.0

        return 0.75

    # If no specific field is mentioned, matching degree
    # level is enough.
    if (
        candidate_level
        and required_level
        and candidate_level == required_level
    ):
        return 1.0

    # Exact normalized text match.
    if candidate == required:
        return 1.0

    return 0.0


def match_education(
    candidate: CandidateProfile,
    job: JobProfile,
) -> dict:
    """
    Compare candidate education against job education requirements.
    """

    requirements = job.education_requirements

    if not requirements:
        return {
            "matched": [],
            "missing": [],
            "score": 1.0,
            "met": True,
        }

    candidate_degrees = [
        education.degree
        for education in candidate.education
    ]

    matched = []
    missing = []

    for requirement in requirements:

        best_score = 0.0

        for candidate_degree in candidate_degrees:
            score = education_match_score(
                candidate_degree,
                requirement,
            )

            best_score = max(
                best_score,
                score,
            )

        if best_score >= 0.75:
            matched.append(requirement)
        else:
            missing.append(requirement)

    score = (
        len(matched) / len(requirements)
    )

    return {
        "matched": matched,
        "missing": missing,
        "score": round(score, 3),
        "met": len(missing) == 0,
    }