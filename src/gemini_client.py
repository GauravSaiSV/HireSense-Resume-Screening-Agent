import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def get_gemini_model() -> str:
    model = os.getenv("GEMINI_MODEL")

    if not model:
        raise ValueError(
            "GEMINI_MODEL is not configured. "
            "Add it to your .env file."
        )

    return model