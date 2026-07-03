import json
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

MODEL_OPTIONS = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]


def generate_final_analysis(nlp_analysis):
    api_key = os.getenv("GEMINI_API_KEY") 

    if not api_key:
        return {
            "status": "missing_api_key",
            "message": "GEMINI_API_KEY is not set. Add your Gemini API key to use final AI explanation."
        }

    prompt = build_analysis_prompt(nlp_analysis)
    client = genai.Client(api_key=api_key)

    last_error = None

    for model_name in MODEL_OPTIONS:
        try:
            response = client.interactions.create(
                model=model_name,
                input=prompt
            )

            return {
                "status": "success",
                "model": model_name,
                "final_analysis": response.output_text
            }

        except Exception as error:
            last_error = str(error)

    return {
        "status": "gemini_error",
        "message": "Gemini could not generate the final explanation right now.",
        "error": last_error
    }


def build_compact_nlp_context(nlp_analysis):
    keywords = nlp_analysis.get("keywords", [])[:8]
    concepts = nlp_analysis.get("concepts", [])[:5]
    statistics = nlp_analysis.get("statistics", {})
    cleaned_text = nlp_analysis.get("cleaned_text", "")
    analysis_mode = nlp_analysis.get("analysis_mode", "unknown")

    compact_concepts = []

    for concept in concepts:
        related = concept.get("related_paragraphs", [])
        top_paragraph = related[0].get("paragraph", "") if related else ""

        compact_concepts.append({
            "concept": concept.get("concept"),
            "importance_score": concept.get("importance_score"),
            "most_relevant_paragraph": top_paragraph[:350]
        })

    if analysis_mode == "fast_classical_nlp":
        cleaned_text_limit = 2500
    else:
        cleaned_text_limit = 1000

    return {
        "analysis_mode": analysis_mode,
        "statistics": statistics,
        "top_keywords": keywords,
        "top_concepts": compact_concepts,
        "cleaned_text_preview": cleaned_text[:cleaned_text_limit]
    }


def build_analysis_prompt(nlp_analysis):
    compact_context = build_compact_nlp_context(nlp_analysis)
    nlp_json = json.dumps(compact_context, indent=2)

    prompt = f"""
You are an expert notes analyzer and teacher.

Write in a formal report style.
Do not directly address the user using words like "you", "your", or "user".
Use "the notes" or "the learner" instead.

Use the compact NLP analysis below to create a detailed study report.

If analysis_mode is fast_classical_nlp:
- Use the cleaned text preview and keywords.
- Do not mention transformer concepts.

If analysis_mode is advanced_transformer_nlp:
- Use the keywords, concepts, and relevant paragraphs.
- Mention semantic concept extraction only if useful.

Create these sections:

1. Topic title
2. What the notes are about
3. Detailed explanation
4. Important definitions
5. Important types or categories
6. Weak or unclear areas
7. Exam-style questions and answers
8. Flashcards
9. Revision plan

COMPACT NLP ANALYSIS:
{nlp_json}
"""

    return prompt