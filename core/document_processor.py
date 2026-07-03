from dataclasses import dataclass
from pathlib import Path

from pdf_handler import extract_text_from_pdf
from ocr.ocr_router import extract_text_from_image

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
PDF_EXTENSIONS = {".pdf"}
@dataclass
class DocumentExtraction:
    file_name: str
    file_type: str
    extracted_text: str
    extraction_method: str


def extract_document(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in PDF_EXTENSIONS:
        text = extract_text_from_pdf(path)

        return DocumentExtraction(
            file_name=path.name,
            file_type="pdf",
            extracted_text=text,
            extraction_method="pdf_text_extraction"
        )

    if extension in IMAGE_EXTENSIONS:
        text, engine = extract_text_from_image(str(path))

        return DocumentExtraction(
            file_name=path.name,
            file_type="image",
            extracted_text=text,
            extraction_method=f"ocr_{engine}"
        )

    raise ValueError(f"Unsupported file type: {extension}")