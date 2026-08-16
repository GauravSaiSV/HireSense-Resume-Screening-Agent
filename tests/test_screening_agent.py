from src.agent.screening_agent import screen_candidates


def test_screening_agent_imports():
    assert callable(screen_candidates)