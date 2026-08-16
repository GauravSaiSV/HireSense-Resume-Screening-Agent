from src.gemini_client import get_gemini_client, get_gemini_model


def main():
    client = get_gemini_client()
    model = get_gemini_model()

    print(f"Testing model: {model}")

    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: Gemini connection successful"
    )

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()