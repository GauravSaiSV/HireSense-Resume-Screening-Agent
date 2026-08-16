from pprint import pprint

from src.agent.screening_agent import screen_candidates


def main():
    job_description = "data/job_description.txt"

    resumes = [
        "data/resumes/test_resume.pdf",
    ]

    print("Starting HireSense screening...")
    print()

    result = screen_candidates(
        job_description_path=job_description,
        resume_paths=resumes,
    )

    print("=" * 70)
    print("HIRÉSENSE SCREENING RESULTS")
    print("=" * 70)

    print("\nJOB PROFILE")
    print("-" * 70)

    job = result["job_profile"]

    print(f"Job title: {job.get('job_title')}")

    print("\nREQUIRED SKILLS:")
    for skill in job.get("required_skills", []):
        print(f"  - {skill}")

    print("\nPREFERRED SKILLS:")
    for skill in job.get("preferred_skills", []):
        print(f"  - {skill}")

    print("\n" + "=" * 70)
    print("CANDIDATE RANKING")
    print("=" * 70)

    for candidate in result["candidates"]:
        print()
        print(f"Rank: {candidate['rank']}")
        print(f"Name: {candidate['candidate_name']}")
        print(f"Final Score: {candidate['final_score']}%")

        print("\nScore Breakdown:")

        for component, score in candidate["breakdown"].items():
            print(f"  {component}: {score * 100:.2f}%")

        print("\nMatched Details:")
        pprint(candidate["details"])

        print("-" * 70)


if __name__ == "__main__":
    main()