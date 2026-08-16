from pathlib import Path
from typing import Any

from src.parser import extract_text
from src.jd_extractor import extract_job_profile
from src.extractor import extract_candidate_profile

from src.scoring.scorer import score_candidate
from src.scoring.ranker import rank_candidates


def screen_candidates(
    job_description_path: str,
    resume_paths: list[str],
) -> dict[str, Any]:
    """
    Run the complete HireSense resume screening workflow.

    Workflow:
    1. Extract job description text.
    2. Convert JD into a structured JobProfile.
    3. Extract each resume's text.
    4. Convert each resume into a CandidateProfile.
    5. Score every candidate against the job.
    6. Rank candidates by final score.
    """

    if not job_description_path:
        raise ValueError("Job description path cannot be empty.")

    if not resume_paths:
        raise ValueError("At least one resume is required.")

    # Validate job description
    job_path = Path(job_description_path)

    if not job_path.exists():
        raise FileNotFoundError(
            f"Job description not found: {job_description_path}"
        )

    # Validate resumes
    for resume_path in resume_paths:
        if not Path(resume_path).exists():
            raise FileNotFoundError(
                f"Resume not found: {resume_path}"
            )

    # Extract job description
    job_text = extract_text(str(job_path))
    job_profile = extract_job_profile(job_text)

    # Process resumes
    scored_candidates = []

    for resume_path in resume_paths:
        resume_text = extract_text(resume_path)

        candidate_profile = extract_candidate_profile(
            resume_text
        )

        result = score_candidate(
            candidate=candidate_profile,
            job=job_profile,
        )

        result["candidate_profile"] = candidate_profile.model_dump()
        result["resume_path"] = resume_path

        scored_candidates.append(result)

    # Rank candidates
    ranked_candidates = rank_candidates(
        scored_candidates
    )

    # Add rank
    for index, candidate in enumerate(
        ranked_candidates,
        start=1,
    ):
        candidate["rank"] = index

    return {
        "job_profile": job_profile.model_dump(),
        "candidates": ranked_candidates,
    }