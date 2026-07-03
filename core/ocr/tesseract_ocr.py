import pytesseract
from PIL import Image

def tesseract_extract(image_path):
    data = pytesseract.image_to_data(
        Image.open(image_path),
        output_type=pytesseract.Output.DICT
    )

    text = []
    confidences = []

    for i in range(len(data["text"])):
        if int(data["conf"][i]) > -1:
            text.append(data["text"][i])
            confidences.append(int(data["conf"][i]))

    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    final_text = " ".join(text)

    return final_text.strip(), avg_conf
