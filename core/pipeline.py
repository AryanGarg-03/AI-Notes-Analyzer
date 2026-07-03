from document_processor import extract_document
from nlp.notes_analyzer import analyze_notes_with_nlp
from llm.gemini_analyzer import generate_final_analysis
from llm.vision_extractor import extract_handwritten_text


def process_notes(file_path):
    document_result = extract_document(file_path)

    nlp_analysis = analyze_notes_with_nlp(
        document_result.extracted_text,
        threshold_chars=5000
    )

    final_ai_analysis = generate_final_analysis(nlp_analysis)

    result = {
        "file_info": {
            "file_name": document_result.file_name,
            "file_type": document_result.file_type,
            "extraction_method": document_result.extraction_method,
            "analysis_mode": nlp_analysis["analysis_mode"]
        },
        "extracted_text": document_result.extracted_text,
        "nlp_analysis": nlp_analysis,
        "final_ai_analysis": final_ai_analysis
    }

    return result


def process_handwritten_notes(image_path):
    handwriting_result = extract_handwritten_text(image_path)

    if handwriting_result["status"] != "success":
        return {
            "file_info": {
                "file_name": image_path,
                "file_type": "image",
                "extraction_method": "gemini_vision",
                "analysis_mode": "vision_failed"
            },
            "extracted_text": "",
            "nlp_analysis": {},
            "final_ai_analysis": handwriting_result
        }

    extracted_text = handwriting_result["text"]

    nlp_analysis = analyze_notes_with_nlp(
        extracted_text,
        threshold_chars=5000
    )

    final_ai_analysis = generate_final_analysis(nlp_analysis)

    return {
        "file_info": {
            "file_name": image_path,
            "file_type": "image",
            "extraction_method": f"gemini_vision_{handwriting_result['model']}",
            "analysis_mode": nlp_analysis["analysis_mode"]
        },
        "extracted_text": extracted_text,
        "nlp_analysis": nlp_analysis,
        "final_ai_analysis": final_ai_analysis
    }