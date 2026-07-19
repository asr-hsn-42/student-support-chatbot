import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "models/gemini-flash-lite-latest"


def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the response text.
    """
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"