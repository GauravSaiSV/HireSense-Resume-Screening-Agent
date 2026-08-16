from src.gemini_client import get_gemini_client, get_gemini_model
from src.models import JobProfile


JD_EXTRACTION_PROMPT = """
You are a job description information extraction system.

Your task is to extract factual information from the job description
and return it using the provided JobProfile schema.

STRICT RULES:

1. Only extract information explicitly supported by the job description.
2. Never invent requirements, skills, experience, education,
   certifications, responsibilities, or keywords.
3. If information is missing, use null for optional scalar fields
   and an empty list for list fields.
4. Separate required skills from preferred or nice-to-have skills.
5. Only place a skill in required_skills if the job description
   clearly indicates that the skill is required.
6. Only place a skill in preferred_skills if the job description
   clearly indicates that the skill is preferred, desirable,
   or nice-to-have.
7. Do not assume that a preferred skill is required.
8. Extract the minimum experience requirement only when the
   job description explicitly provides one.
9. Do not convert vague statements such as "experienced" into
   a specific number of years.
10. Extract responsibilities as concise statements while
    preserving their original meaning.
11. Keywords should contain important job-specific terms that
    are explicitly present in the job description.
12. Return only information relevant to the JobProfile schema.

JOB DESCRIPTION:

{job_description}
"""


def extract_job_profile(job_description: str) -> JobProfile:
    """
    Extract a structured job profile from a job description using Gemini.
    """

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    client = get_gemini_client()
    model = get_gemini_model()

    prompt = JD_EXTRACTION_PROMPT.format(
        job_description=job_description
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JobProfile,
        },
    )

    if not response.parsed:
        raise ValueError(
            "Gemini returned no structured job profile."
        )

    return response.parsed