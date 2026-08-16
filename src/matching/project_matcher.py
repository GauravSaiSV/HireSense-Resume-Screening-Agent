import re

from src.models import CandidateProfile, JobProfile
from src.matching.normalizer import canonicalize_skills


def normalize_text(text: str) -> str:
    """
    Normalize text for simple keyword comparison.
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


def project_relevance_score(
    project: str,
    job: JobProfile,
) -> float:
    """
    Calculate a deterministic relevance score for a project
    based on overlap with job skills, responsibilities and keywords.

    Returns a value between 0.0 and 1.0.
    """

    if not project:
        return 0.0

    project_text = normalize_text(project)

    # Canonicalize job skills.
    job_skills = canonicalize_skills(
        job.required_skills
        + job.preferred_skills
    )

    matched_skills = 0

    for skill in job_skills:
        if normalize_text(skill) in project_text:
            matched_skills += 1

    skill_score = (
        matched_skills / len(job_skills)
        if job_skills
        else 0.0
    )

    # Compare against job keywords.
    keywords = [
        normalize_text(keyword)
        for keyword in job.keywords
        if keyword
    ]

    matched_keywords = sum(
        1
        for keyword in keywords
        if keyword in project_text
    )

    keyword_score = (
        matched_keywords / len(keywords)
        if keywords
        else 0.0
    )

    # Compare against responsibilities.
    responsibility_matches = 0

    for responsibility in job.responsibilities:
        responsibility_words = set(
            normalize_text(responsibility).split()
        )

        project_words = set(
            project_text.split()
        )

        if not responsibility_words:
            continue

        overlap = (
            responsibility_words
            & project_words
        )

        # Ignore very small overlaps.
        if len(overlap) >= 2:
            responsibility_matches += 1

    responsibility_score = (
        responsibility_matches
        / len(job.responsibilities)
        if job.responsibilities
        else 0.0
    )

    # Weighted project relevance.
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