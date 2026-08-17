from src.gemini_client import get_gemini_client, get_gemini_model
from src.models import CandidateProfile


EXTRACTION_PROMPT = """
You are a resume information extraction system.

Your task is to extract factual information from the resume text
and return it using the provided CandidateProfile schema.

STRICT RULES:

1. Only extract information explicitly supported by the resume.

2. Never invent or assume skills, education, companies, job titles,
   achievements, certifications, dates, or experience.

3. If information is missing, use null for optional scalar fields
   and an empty list for list fields.

4. Preserve the meaning of the candidate's information.

5. Do not add skills merely because they are related to another skill.
   For example, do not infer PyTorch from TensorFlow.

6. Do not infer employment duration unless the resume explicitly
   provides enough information to determine it.

7. For each work experience entry, extract the start date and end date
   when they are explicitly present in the resume.

8. If the resume explicitly says "Present" for an employment end date,
   preserve "Present" as the end date.

9. Never invent, estimate, or assume missing employment dates.

10. Preserve the duration exactly as stated in the resume when a duration
    is explicitly provided. Do not calculate or estimate a duration
    unless the resume itself provides enough explicit date information.

11. Projects must preserve the full project information explicitly
    available in the resume.

    For each project, include:
    - the project title/name
    - the project description
    - technologies, frameworks, libraries, or tools explicitly
      mentioned for that project
    - important technical methods or concepts explicitly mentioned

    Combine this information into a single string for each project.

    Do not reduce a project to only its title.

    Example:
    If the resume says:

        Image Classification System
        Built an image classification system using Python,
        TensorFlow and deep learning.

    Return:

        "Image Classification System - Built an image classification
        system using Python, TensorFlow and deep learning."

    Only include information explicitly present in the resume.
    Never invent technologies or project details.

12. Certifications should contain certifications explicitly mentioned
    in the resume.

13. Return only information relevant to the CandidateProfile schema.

RESUME TEXT:

{resume_text}
"""


def extract_candidate_profile(resume_text: str) -> CandidateProfile:
    """
    Extract a structured candidate profile from resume text using Gemini.
    """

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    client = get_gemini_client()
    model = get_gemini_model()

    prompt = EXTRACTION_PROMPT.format(
        resume_text=resume_text
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CandidateProfile,
        },
    )

    if not response.parsed:
        raise ValueError(
            "Gemini returned no structured candidate profile."
        )

    return response.parsed