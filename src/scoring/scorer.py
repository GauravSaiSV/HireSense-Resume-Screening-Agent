from src.models import CandidateProfile, JobProfile

from src.matching.skill_matcher import match_skills
from src.matching.experience_matcher import match_experience
from src.matching.education_matcher import match_education
from src.matching.project_matcher import match_projects


WEIGHTS = {
    "required_skills": 0.40,
    "preferred_skills": 0.15,
    "experience": 0.20,
    "education": 0.10,
    "projects": 0.15,
}


def calculate_weighted_score(
    required_skills_score: float,
    preferred_skills_score: float,
    experience_score: float,
    education_score: float,
    project_score: float,
) -> float:
    """
    Calculate the final weighted candidate score.

    Input scores must be between 0.0 and 1.0.
    Returns a percentage between 0 and 100.
    """

    component_scores = [
        required_skills_score,
        preferred_skills_score,
        experience_score,
        education_score,
        project_score,
    ]

    if not all(0.0 <= score <= 1.0 for score in component_scores):
        raise ValueError(
            "All component scores must be between 0.0 and 1.0."
        )

    score = (
        required_skills_score * WEIGHTS["required_skills"]
        + preferred_skills_score * WEIGHTS["preferred_skills"]
        + experience_score * WEIGHTS["experience"]
        + education_score * WEIGHTS["education"]
        + project_score * WEIGHTS["projects"]
    )

    return round(score * 100, 2)


def score_candidate(
    candidate: CandidateProfile,
    job: JobProfile,
) -> dict:
    """
    Run all matching components and produce
    an explainable candidate score.
    """

    skill_result = match_skills(candidate, job)

    experience_result = match_experience(candidate, job)

    education_result = match_education(candidate, job)

    project_result = match_projects(candidate, job)

    final_score = calculate_weighted_score(
        required_skills_score=skill_result["required"]["score"],
        preferred_skills_score=skill_result["preferred"]["score"],
        experience_score=experience_result["score"],
        education_score=education_result["score"],
        project_score=project_result["best_score"],
    )

    return {
        "candidate_name": candidate.name,
        "final_score": final_score,

        "breakdown": {
            "required_skills": skill_result["required"]["score"],
            "preferred_skills": skill_result["preferred"]["score"],
            "experience": experience_result["score"],
            "education": education_result["score"],
            "projects": project_result["best_score"],
        },

        "details": {
            "skills": skill_result,
            "experience": experience_result,
            "education": education_result,
            "projects": project_result,
        },
    }