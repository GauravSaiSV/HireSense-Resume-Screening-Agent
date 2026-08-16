import re
from datetime import date
from typing import Optional

from src.models import CandidateProfile, JobProfile


MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def parse_date(value: Optional[str]) -> Optional[tuple[int, int]]:
    """
    Parse a resume date into (year, month).

    Supported examples:
        2024
        Jan 2024
        January 2024
        01/2024
        2024/01
    """

    if not value:
        return None

    value = value.strip().lower()

    # Ignore "Present" here.
    if value == "present":
        return None

    # Month name + year, e.g. "Jan 2024"
    month_pattern = (
        r"\b("
        + "|".join(MONTHS.keys())
        + r")\s+"
        r"(19\d{2}|20\d{2})\b"
    )

    match = re.search(month_pattern, value)

    if match:
        month_name = match.group(1)
        year = int(match.group(2))

        return year, MONTHS[month_name]

    # MM/YYYY or MM-YYYY
    match = re.search(
        r"\b(0?[1-9]|1[0-2])[-/](19\d{2}|20\d{2})\b",
        value,
    )

    if match:
        month = int(match.group(1))
        year = int(match.group(2))

        return year, month

    # YYYY/MM or YYYY-MM
    match = re.search(
        r"\b(19\d{2}|20\d{2})[-/](0?[1-9]|1[0-2])\b",
        value,
    )

    if match:
        year = int(match.group(1))
        month = int(match.group(2))

        return year, month

    # Year only
    match = re.search(
        r"\b(19\d{2}|20\d{2})\b",
        value,
    )

    if match:
        year = int(match.group(1))

        # When only a year is provided, use January.
        return year, 1

    return None


def calculate_months_between(
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    """
    Calculate the number of months between two (year, month) values.
    """

    start_year, start_month = start
    end_year, end_month = end

    return (
        (end_year - start_year) * 12
        + (end_month - start_month)
    )


def calculate_experience_years(
    candidate: CandidateProfile,
) -> Optional[float]:
    """
    Calculate total professional experience in years.

    Returns None when no usable experience dates are available.
    """

    total_months = 0

    current_date = date.today()

    current = (
        current_date.year,
        current_date.month,
    )

    for experience in candidate.experience:

        start = parse_date(
            experience.start_date
        )

        if start is None:
            continue

        if (
            experience.end_date
            and experience.end_date.strip().lower() == "present"
        ):
            end = current
        else:
            end = parse_date(
                experience.end_date
            )

        if end is None:
            continue

        months = calculate_months_between(
            start,
            end,
        )

        if months > 0:
            total_months += months

    if total_months == 0:
        return None

    return round(
        total_months / 12,
        1,
    )


def match_experience(
    candidate: CandidateProfile,
    job: JobProfile,
) -> dict:
    """
    Compare candidate experience against the job's
    minimum experience requirement.
    """

    required_years = (
        job.minimum_experience_years
    )

    candidate_years = (
        calculate_experience_years(candidate)
    )

    # No experience requirement.
    if required_years is None:
        return {
            "required_years": None,
            "candidate_years": candidate_years,
            "met": True,
            "score": 1.0,
        }

    # Requirement exists, but candidate has no
    # usable date information.
    if candidate_years is None:
        return {
            "required_years": required_years,
            "candidate_years": None,
            "met": False,
            "score": 0.0,
        }

    # Requirement satisfied.
    if candidate_years >= required_years:
        return {
            "required_years": required_years,
            "candidate_years": candidate_years,
            "met": True,
            "score": 1.0,
        }

    # Partial score when candidate has less experience
    # than required.
    score = candidate_years / required_years

    return {
        "required_years": required_years,
        "candidate_years": candidate_years,
        "met": False,
        "score": round(score, 3),
    }