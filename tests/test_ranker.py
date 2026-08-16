from src.scoring.ranker import rank_candidates


def test_rank_candidates_descending():
    candidates = [
        {
            "candidate_name": "Candidate A",
            "final_score": 72.5,
        },
        {
            "candidate_name": "Candidate B",
            "final_score": 91.0,
        },
        {
            "candidate_name": "Candidate C",
            "final_score": 84.25,
        },
    ]

    result = rank_candidates(candidates)

    assert [
        candidate["candidate_name"]
        for candidate in result
    ] == [
        "Candidate B",
        "Candidate C",
        "Candidate A",
    ]


def test_rank_candidates_preserves_score():
    candidates = [
        {
            "candidate_name": "Candidate A",
            "final_score": 72.5,
        },
        {
            "candidate_name": "Candidate B",
            "final_score": 91.0,
        },
    ]

    result = rank_candidates(candidates)

    assert result[0]["final_score"] == 91.0
    assert result[1]["final_score"] == 72.5


def test_equal_scores_preserve_original_order():
    candidates = [
        {
            "candidate_name": "Candidate A",
            "final_score": 85.0,
        },
        {
            "candidate_name": "Candidate B",
            "final_score": 85.0,
        },
        {
            "candidate_name": "Candidate C",
            "final_score": 85.0,
        },
    ]

    result = rank_candidates(candidates)

    assert [
        candidate["candidate_name"]
        for candidate in result
    ] == [
        "Candidate A",
        "Candidate B",
        "Candidate C",
    ]


def test_empty_candidate_list():
    result = rank_candidates([])

    assert result == []