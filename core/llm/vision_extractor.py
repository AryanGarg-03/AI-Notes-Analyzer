import os

from google import genai
from dotenv import load_dotenv
load_dotenv()
MODEL_OPTIONS = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]


def extract_handwritten_text(image_path):
    api_key = os.getenv("GEMINI_API_KEY") 

    if not api_key:
        return {
            "status": "missing_api_key",
            "text": "",
            "message": "GEMINI_API_KEY is not set."
        }

    client = genai.Client(api_key=api_key)

    prompt = """
Read the handwritten notes in this image carefully.

Return only the extracted text.
Do not explain it.
Do not summarize it.
If a word is unclear, write [unclear].
Keep the original order of the notes as much as possible.
"""

    last_error = None

    for model_name in MODEL_OPTIONS:
        try:
            uploaded_file = client.files.upload(file=image_path)

            response = client.interactions.create(
                model=model_name,
                input=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "uri": uploaded_file.uri,
                        "mime_type": uploaded_file.mime_type
                    }
                ]
            )

            return {
                "status": "success",
                "model": model_name,
                "text": response.output_text
            }

        except Exception as error:
            last_error = str(error)

    return {
        "status": "vision_error",
        "text": "",
        "message": "Gemini Vision could not read the handwritten image.",
        "error": last_error
    }