from typing import Optional

from pydantic import BaseModel, Field


class Experience(BaseModel):
    title: str = Field(
        description="Job title or role mentioned in the resume."
    )

    company: Optional[str] = Field(
        default=None,
        description="Company or organization name if explicitly mentioned."
    )

    start_date: Optional[str] = Field(
        default=None,
        description="Start date exactly as stated in the resume."
    )

    end_date: Optional[str] = Field(
        default=None,
        description="End date exactly as stated in the resume. Preserve 'Present' if explicitly stated."
    )

    duration: Optional[str] = Field(
        default=None,
        description="Employment duration exactly as stated in the resume."
    )

    description: str = Field(
        description="Summary of responsibilities and achievements explicitly supported by the resume."
    )


class Education(BaseModel):
    degree: str = Field(
        description="Degree, qualification, or course name."
    )
    institution: Optional[str] = Field(
        default=None,
        description="Educational institution if explicitly mentioned."
    )
    year: Optional[str] = Field(
        default=None,
        description="Graduation or completion year if explicitly mentioned."
    )


class CandidateProfile(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Candidate's full name if present."
    )

    email: Optional[str] = Field(
        default=None,
        description="Candidate's email address if present."
    )

    phone: Optional[str] = Field(
        default=None,
        description="Candidate's phone number if present."
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Technical and professional skills explicitly mentioned in the resume."
    )

    education: list[Education] = Field(
        default_factory=list,
        description="Educational qualifications explicitly mentioned in the resume."
    )

    experience: list[Experience] = Field(
        default_factory=list,
        description="Work experience, internships, and other professional experience explicitly mentioned."
    )

    projects: list[str] = Field(
        default_factory=list,
        description="Projects explicitly mentioned in the resume."
    )

    certifications: list[str] = Field(
        default_factory=list,
        description="Certifications explicitly mentioned in the resume."
    )

    total_experience_years: Optional[float] = Field(
        default=None,
        description="Total professional experience in years only when it can be reasonably determined from the resume."
    )

class JobProfile(BaseModel):
    job_title: Optional[str] = Field(
        default=None,
        description="Job title explicitly stated in the job description."
    )

    required_skills: list[str] = Field(
        default_factory=list,
        description="Skills explicitly required for the role."
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
        description="Skills explicitly preferred, desirable, or nice-to-have."
    )

    minimum_experience_years: Optional[float] = Field(
        default=None,
        description="Minimum years of experience explicitly required."
    )

    education_requirements: list[str] = Field(
        default_factory=list,
        description="Educational qualifications explicitly required or preferred."
    )

    responsibilities: list[str] = Field(
        default_factory=list,
        description="Major responsibilities explicitly stated in the job description."
    )

    certifications: list[str] = Field(
        default_factory=list,
        description="Required or preferred certifications explicitly mentioned."
    )

    keywords: list[str] = Field(
        default_factory=list,
        description="Important job-specific keywords explicitly present in the job description."
    )