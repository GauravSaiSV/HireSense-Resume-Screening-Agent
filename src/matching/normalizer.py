import re


SKILL_ALIASES = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "ai": "artificial intelligence",
    "ai/ml": "artificial intelligence and machine learning",
    "aiml": "artificial intelligence and machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "postgres db": "postgresql",
    "postgres database": "postgresql",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tf": "tensorflow",
    "k8s": "kubernetes",
    "gcp": "google cloud",
}


CANONICAL_SKILLS = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "nosql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "opencv",
    "fastapi",
    "flask",
    "django",
    "rest api",
    "git",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "spark",
    "hadoop",
}


def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill phrase.
    """

    if not skill:
        return ""

    normalized = skill.lower().strip()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    normalized = normalized.replace("_", " ")

    if normalized in SKILL_ALIASES:
        normalized = SKILL_ALIASES[normalized]

    return normalized


def canonicalize_skill(skill: str) -> list[str]:
    """
    Convert a potentially broad skill phrase into one or more
    canonical skills from the known vocabulary.
    """

    normalized = normalize_skill(skill)

    if not normalized:
        return []

    # Exact canonical skill.
    if normalized in CANONICAL_SKILLS:
        return [normalized]

    matches = []

    # Look for known skills contained in the phrase.
    for canonical_skill in CANONICAL_SKILLS:
        if canonical_skill in normalized:
            matches.append(canonical_skill)

    return matches


def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize and deduplicate a list of skills.
    """

    normalized = []

    for skill in skills:
        value = normalize_skill(skill)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


def canonicalize_skills(skills: list[str]) -> list[str]:
    """
    Convert a list of extracted skill phrases into canonical skills.
    """

    canonical = []

    for skill in skills:
        matches = canonicalize_skill(skill)

        for match in matches:
            if match not in canonical:
                canonical.append(match)

    return canonical