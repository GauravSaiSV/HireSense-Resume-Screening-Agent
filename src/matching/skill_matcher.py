from src.models import CandidateProfile, JobProfile
from src.matching.normalizer import canonicalize_skills


def match_skills(
    candidate: CandidateProfile,
    job: JobProfile,
) -> dict:
    """
    Compare candidate skills against required and preferred
    job skills using canonical skill matching.
    """

    candidate_skills = set(
        canonicalize_skills(candidate.skills)
    )

    required_skills = canonicalize_skills(
        job.required_skills
    )

    preferred_skills = canonicalize_skills(
        job.preferred_skills
    )

    matched_required = []
    missing_required = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    matched_preferred = []
    missing_preferred = []

    for skill in preferred_skills:
        if skill in candidate_skills:
            matched_preferred.append(skill)
        else:
            missing_preferred.append(skill)

    required_score = (
        len(matched_required) / len(required_skills)
        if required_skills
        else 1.0
    )

    preferred_score = (
        len(matched_preferred) / len(preferred_skills)
        if preferred_skills
        else 1.0
    )

    return {
        "required": {
            "matched": matched_required,
            "missing": missing_required,
            "score": required_score,
        },
        "preferred": {
            "matched": matched_preferred,
            "missing": missing_preferred,
            "score": preferred_score,
        },
    }