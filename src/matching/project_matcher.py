import re

from src.models import CandidateProfile, JobProfile
from src.matching.normalizer import canonicalize_skills


# ---------------------------------------------------------
# Domain concept aliases
# ---------------------------------------------------------
#
# These represent concepts that are strongly related in
# machine-learning projects.
#
# This is deterministic domain knowledge, not LLM inference.
#

CONCEPT_ALIASES = {
    "deep learning": "machine learning",
    "neural network": "machine learning",
    "neural networks": "machine learning",
    "machine learning model": "machine learning",
    "machine learning models": "machine learning",
    "ml model": "machine learning",
    "ml models": "machine learning",
    "model training": "machine learning",
    "model development": "machine learning",

    "image classification": "machine learning",
    "text classification": "machine learning",
    "classification model": "machine learning",
    "classification models": "machine learning",

    "object detection": "computer vision",
    "image recognition": "computer vision",
    "image processing": "computer vision",
}


def normalize_text(text: str) -> str:
    """
    Normalize text for keyword and concept comparison.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def expand_concepts(text: str) -> set[str]:
    """
    Convert text into a set of normalized concepts.

    Exact words/phrases are retained and known domain concepts
    are additionally mapped to canonical concepts.
    """

    normalized = normalize_text(text)

    concepts = set()

    if normalized:
        concepts.add(normalized)

    for phrase, canonical in CONCEPT_ALIASES.items():
        if phrase in normalized:
            concepts.add(canonical)

    return concepts


def phrase_matches(
    phrase: str,
    project_text: str,
) -> bool:
    """
    Determine whether a phrase is explicitly present in the
    project or is represented by a known domain concept.
    """

    normalized_phrase = normalize_text(phrase)

    if not normalized_phrase:
        return False

    # Direct phrase match
    if normalized_phrase in project_text:
        return True

    # Check whether the job phrase maps to a known concept
    canonical_phrase = CONCEPT_ALIASES.get(
        normalized_phrase
    )

    if canonical_phrase:
        if canonical_phrase in project_text:
            return True

        # Check whether the project contains an alias
        for alias, canonical in CONCEPT_ALIASES.items():
            if canonical == canonical_phrase:
                if alias in project_text:
                    return True

    # Check whether the project contains a concept
    # that maps to the job phrase.
    for alias, canonical in CONCEPT_ALIASES.items():
        if alias in project_text and canonical == normalized_phrase:
            return True

    return False


def project_relevance_score(
    project: str,
    job: JobProfile,
) -> float:
    """
    Calculate a deterministic relevance score for a project
    based on overlap with job skills, responsibilities and
    keywords.

    Returns a value between 0.0 and 1.0.
    """

    if not project:
        return 0.0

    project_text = normalize_text(project)

    # ---------------------------------------------------------
    # 1. Job skills
    # ---------------------------------------------------------

    job_skills = canonicalize_skills(
        job.required_skills
        + job.preferred_skills
    )

    matched_skills = 0

    for skill in job_skills:
        if phrase_matches(
            skill,
            project_text,
        ):
            matched_skills += 1

    skill_score = (
        matched_skills / len(job_skills)
        if job_skills
        else 0.0
    )

    # ---------------------------------------------------------
    # 2. Job keywords
    # ---------------------------------------------------------

    keywords = [
        normalize_text(keyword)
        for keyword in job.keywords
        if keyword
    ]

    matched_keywords = sum(
        1
        for keyword in keywords
        if phrase_matches(
            keyword,
            project_text,
        )
    )

    keyword_score = (
        matched_keywords / len(keywords)
        if keywords
        else 0.0
    )

    # ---------------------------------------------------------
    # 3. Responsibilities
    # ---------------------------------------------------------

    responsibility_matches = 0

    project_words = set(
        project_text.split()
    )

    for responsibility in job.responsibilities:

        responsibility_text = normalize_text(
            responsibility
        )

        if not responsibility_text:
            continue

        responsibility_words = set(
            responsibility_text.split()
        )

        overlap = (
            responsibility_words
            & project_words
        )

        # Existing deterministic overlap rule.
        if len(overlap) >= 2:
            responsibility_matches += 1

        # Also recognize strong ML concept relationships.
        else:
            responsibility_concepts = expand_concepts(
                responsibility_text
            )

            project_concepts = expand_concepts(
                project_text
            )

            if responsibility_concepts & project_concepts:
                responsibility_matches += 1

    responsibility_score = (
        responsibility_matches
        / len(job.responsibilities)
        if job.responsibilities
        else 0.0
    )

    # ---------------------------------------------------------
    # 4. Final project score
    # ---------------------------------------------------------

    score = (
        skill_score * 0.50
        + keyword_score * 0.20
        + responsibility_score * 0.30
    )

    return round(
        min(score, 1.0),
        3,
    )


def match_projects(
    candidate: CandidateProfile,
    job: JobProfile,
) -> dict:
    """
    Evaluate all candidate projects against the job.
    """

    if not candidate.projects:
        return {
            "projects": [],
            "average_score": 0.0,
            "best_score": 0.0,
        }

    project_results = []

    for project in candidate.projects:

        score = project_relevance_score(
            project,
            job,
        )

        project_results.append(
            {
                "project": project,
                "score": score,
            }
        )

    scores = [
        result["score"]
        for result in project_results
    ]

    return {
        "projects": project_results,
        "average_score": round(
            sum(scores) / len(scores),
            3,
        ),
        "best_score": max(scores),
    }