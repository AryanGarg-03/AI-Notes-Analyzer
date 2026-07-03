from .tesseract_ocr import tesseract_extract
from .easyocr_ocr import easyocr_extract

CONF_THRESHOLD = 70

def extract_text_from_image(image_path):
    text, confidence = tesseract_extract(image_path)

    if confidence >= CONF_THRESHOLD and len(text) > 20:
        return text, "tesseract"

    text = easyocr_extract(image_path)
    return text, "easyocr"