from tesserocr import PyTessBaseAPI

api = None


def ocr_photo(file: str, lang: str = "pol") -> str:
    """OCR photo file and return text."""
    global api
    if api is None:
        api = PyTessBaseAPI(lang=lang)

    api.SetImageFile(file)

    return api.GetUTF8Text().strip()
