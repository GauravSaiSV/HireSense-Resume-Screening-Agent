import tempfile
from pathlib import Path

import streamlit as st

from src.agent.screening_agent import screen_candidates


st.set_page_config(
    page_title="HireSense",
    page_icon="🎯",
    layout="wide",
)


st.title("HireSense")
st.subheader("AI Resume Screening Agent")

st.write(
    "Upload a job description and candidate resumes "
    "to automatically screen, score, and rank candidates."
)


# ---------------------------------------------------------
# Job Description
# ---------------------------------------------------------

st.header("1. Job Description")

job_description_file = st.file_uploader(
    "Upload Job Description",
    type=["txt", "pdf", "docx"],
    key="job_description",
)


# ---------------------------------------------------------
# Resumes
# ---------------------------------------------------------

st.header("2. Candidate Resumes")

resume_files = st.file_uploader(
    "Upload one or more resumes",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True,
    key="resumes",
)


# ---------------------------------------------------------
# Screening
# ---------------------------------------------------------

st.header("3. Screen Candidates")

if st.button(
    "Screen Candidates",
    type="primary",
    use_container_width=True,
):

    if job_description_file is None:
        st.error(
            "Please upload a job description."
        )
        st.stop()

    if not resume_files:
        st.error(
            "Please upload at least one resume."
        )
        st.stop()

    with st.spinner(
        "Analyzing job description and resumes..."
    ):

        try:
            # Temporary directory for uploaded files.
            with tempfile.TemporaryDirectory() as temp_dir:

                temp_path = Path(temp_dir)

                # Save job description.
                job_path = (
                    temp_path
                    / job_description_file.name
                )

                job_path.write_bytes(
                    job_description_file.getvalue()
                )

                # Save resumes.
                resume_paths = []

                for resume_file in resume_files:

                    resume_path = (
                        temp_path
                        / resume_file.name
                    )

                    resume_path.write_bytes(
                        resume_file.getvalue()
                    )

                    resume_paths.append(
                        str(resume_path)
                    )

                # Run complete HireSense pipeline.
                result = screen_candidates(
                    job_description_path=str(
                        job_path
                    ),
                    resume_paths=resume_paths,
                )

            st.session_state["screening_result"] = result

            st.success(
                "Screening completed successfully."
            )

        except Exception as exc:

            st.error(
                f"Screening failed: {exc}"
            )


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

result = st.session_state.get(
    "screening_result"
)


if result:

    st.divider()

    st.header("Screening Results")

    job = result["job_profile"]

    st.subheader(
        job.get("job_title")
        or "Job Profile"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Candidates",
            len(result["candidates"]),
        )

    with col2:
        required_count = len(
            job.get(
                "required_skills",
                [],
            )
        )

        st.metric(
            "Required Skills",
            required_count,
        )

    with col3:
        preferred_count = len(
            job.get(
                "preferred_skills",
                [],
            )
        )

        st.metric(
            "Preferred Skills",
            preferred_count,
        )


    # -----------------------------------------------------
    # Candidate ranking
    # -----------------------------------------------------

    st.subheader("Candidate Ranking")

    for candidate in result["candidates"]:

        profile = candidate[
            "candidate_profile"
        ]

        name = (
            profile.get("name")
            or "Unknown Candidate"
        )

        score = candidate[
            "final_score"
        ]

        rank = candidate["rank"]

        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [1, 5, 2]
            )

            with col1:
                st.markdown(
                    f"### #{rank}"
                )

            with col2:
                st.markdown(
                    f"### {name}"
                )

                email = profile.get(
                    "email"
                )

                if email:
                    st.caption(email)

            with col3:
                st.metric(
                    "Score",
                    f"{score:.2f}%",
                )


            # ---------------------------------------------
            # Score breakdown
            # ---------------------------------------------

            st.markdown(
                "**Score Breakdown**"
            )

            breakdown = candidate.get(
                "breakdown",
                {}
            )

            breakdown_columns = st.columns(
                len(breakdown)
                if breakdown
                else 1
            )

            for column, (
                component,
                component_score,
            ) in zip(
                breakdown_columns,
                breakdown.items(),
            ):

                with column:

                    if isinstance(
                        component_score,
                        (int, float),
                    ):

                        st.metric(
                            component.replace(
                                "_",
                                " "
                            ).title(),
                            f"{component_score * 100:.1f}%",
                        )


            # ---------------------------------------------
            # Candidate details
            # ---------------------------------------------

            details = candidate.get(
                "details",
                {}
            )

            with st.expander(
                "View Candidate Details"
            ):

                skills = details.get(
                    "skills",
                    {}
                )

                st.markdown(
                    "#### Skills"
                )

                required = skills.get(
                    "required",
                    {}
                )

                preferred = skills.get(
                    "preferred",
                    {}
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        "**Required Skills**"
                    )

                    matched = required.get(
                        "matched",
                        []
                    )

                    missing = required.get(
                        "missing",
                        []
                    )

                    if matched:
                        st.write(
                            "Matched:"
                        )

                        for skill in matched:
                            st.success(
                                skill
                            )

                    if missing:
                        st.write(
                            "Missing:"
                        )

                        for skill in missing:
                            st.error(
                                skill
                            )

                with col2:

                    st.markdown(
                        "**Preferred Skills**"
                    )

                    matched = preferred.get(
                        "matched",
                        []
                    )

                    missing = preferred.get(
                        "missing",
                        []
                    )

                    if matched:
                        st.write(
                            "Matched:"
                        )

                        for skill in matched:
                            st.success(
                                skill
                            )

                    if missing:
                        st.write(
                            "Missing:"
                        )

                        for skill in missing:
                            st.warning(
                                skill
                            )


                # -----------------------------------------
                # Education
                # -----------------------------------------

                education = details.get("education")

                if education:
                    st.markdown("#### Education")

                    education_matched = education.get("matched", [])
                    education_missing = education.get("missing", [])
                    education_met = education.get("met", False)

                    if education_matched:
                        st.markdown("**Matched Requirements**")

                        for requirement in education_matched:
                            st.success(f"✓ {requirement}")

                    if education_missing:
                        st.markdown("**Missing Requirements**")

                        for requirement in education_missing:
                            st.error(f"✗ {requirement}")

                    if education_met:
                        st.success("Education requirement satisfied.")
                    else:
                        st.warning("Education requirement not satisfied.")

                # -----------------------------------------
                # Experience
                # -----------------------------------------

                experience = details.get("experience")

                if experience:
                    st.markdown("#### Experience")

                    required_years = experience.get("required_years")
                    candidate_years = experience.get("candidate_years")
                    experience_met = experience.get("met", False)

                    col1, col2 = st.columns(2)

                    with col1:
                        if required_years is None:
                            st.metric(
                                "Minimum Required",
                                "Not specified",
                            )
                        else:
                            st.metric(
                                "Minimum Required",
                                f"{required_years:.1f} years",
                            )

                    with col2:
                        if candidate_years is None:
                            st.metric(
                                "Candidate Experience",
                                "Not determinable",
                            )
                        else:
                            st.metric(
                                "Candidate Experience",
                                f"{candidate_years:.1f} years",
                            )

                    if required_years is None:
                        st.info(
                            "The job description does not specify a minimum "
                            "experience requirement."
                        )
                    elif candidate_years is None:
                        st.warning(
                            "Candidate experience could not be determined "
                            "from the available employment dates."
                        )
                    elif experience_met:
                        st.success(
                            "✓ Candidate meets the experience requirement."
                        )
                    else:
                        st.error(
                            "✗ Candidate does not meet the experience requirement."
                        )


                # -----------------------------------------
                # Projects
                # -----------------------------------------

                projects = details.get("projects")

                if projects:
                    st.markdown("#### Projects")

                    project_list = projects.get("projects", [])
                    average_score = projects.get("average_score", 0.0)
                    best_score = projects.get("best_score", 0.0)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Average Relevance",
                            f"{average_score * 100:.1f}%",
                        )

                    with col2:
                        st.metric(
                            "Best Project Match",
                            f"{best_score * 100:.1f}%",
                        )

                    st.markdown("**Project Matches**")

                    for index, project in enumerate(
                        project_list,
                        start=1,
                    ):
                        project_text = project.get(
                            "project",
                            "Unnamed Project",
                        )

                        project_score = project.get(
                            "score",
                            0.0,
                        )

                        st.markdown(
                            f"**Project {index}**"
                        )

                        st.write(project_text)

                        st.progress(
                            min(max(project_score, 0.0), 1.0),
                            text=(
                                f"Relevance: "
                                f"{project_score * 100:.1f}%"
                            ),
                        )