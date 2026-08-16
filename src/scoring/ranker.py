from typing import Any


def rank_candidates(
    scored_candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Rank candidates by final score in descending order.

    Python's sorting algorithm is stable, so candidates with
    identical scores retain their original order.
    """

    if not scored_candidates:
        return []

    return sorted(
        scored_candidates,
        key=lambda candidate: candidate["final_score"],
        reverse=True,
    )