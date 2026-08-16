from src.extractor import extract_candidate_profile
from src.parser import extract_text


def main():
    resume_path = "data/resumes/test_resume.txt"

    print("Reading resume...")
    resume_text = extract_text(resume_path)

    print("Sending resume to Gemini...")
    profile = extract_candidate_profile(resume_text)

    print("\n" + "=" * 60)
    print("EXTRACTED CANDIDATE PROFILE")
    print("=" * 60)

    print(f"\nName: {profile.name}")
    print(f"Email: {profile.email}")
    print(f"Phone: {profile.phone}")

    print("\nSkills:")
    for skill in profile.skills:
        print(f"  - {skill}")

    print("\nEducation:")
    for education in profile.education:
        print(f"  - {education}")

    print("\nExperience:")
    for experience in profile.experience:
        print(f"  - {experience}")

    print("\nProjects:")
    for project in profile.projects:
        print(f"  - {project}")

    print("\nCertifications:")
    for certification in profile.certifications:
        print(f"  - {certification}")

    print(
        f"\nTotal experience: "
        f"{profile.total_experience_years}"
    )


if __name__ == "__main__":
    main()