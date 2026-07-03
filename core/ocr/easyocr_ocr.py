import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def easyocr_extract(image_path):
    result = reader.readtext(image_path)

    text = " ".join([res[1] for res in result])
    return text.strip()

