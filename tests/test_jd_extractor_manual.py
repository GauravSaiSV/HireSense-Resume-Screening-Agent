from pathlib import Path

from src.jd_extractor import extract_job_profile


def main():
    jd_path = Path("data/job_description.txt")

    job_description = jd_path.read_text(
        encoding="utf-8"
    )

    print("Reading job description...")
    print("Sending job description to Gemini...")

    profile = extract_job_profile(job_description)

    print("\n" + "=" * 60)
    print("EXTRACTED JOB PROFILE")
    print("=" * 60)

    print(f"\nJob title: {profile.job_title}")

    print("\nRequired skills:")
    for skill in profile.required_skills:
        print(f"  - {skill}")

    print("\nPreferred skills:")
    for skill in profile.preferred_skills:
        print(f"  - {skill}")

    print(
        f"\nMinimum experience: "
        f"{profile.minimum_experience_years}"
    )

    print("\nEducation requirements:")
    for education in profile.education_requirements:
        print(f"  - {education}")

    print("\nResponsibilities:")
    for responsibility in profile.responsibilities:
        print(f"  - {responsibility}")

    print("\nCertifications:")
    for certification in profile.certifications:
        print(f"  - {certification}")

    print("\nKeywords:")
    for keyword in profile.keywords:
        print(f"  - {keyword}")


if __name__ == "__main__":
    main()