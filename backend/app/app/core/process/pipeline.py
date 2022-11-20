import json
import shutil
from pathlib import Path
from typing import Any, Dict

from app.core.process.extract import download_media, extract_text
from app.core.process.modeling import detect_scam


def run_pipeline(tweet: Dict[str, Any]) -> float:
    """Run pipeline on given tweet."""
    text = tweet["text"].strip()
    tmp_path = Path("/tmp/this-is-fine")
    tmp_path.mkdir(exist_ok=True)
    download_media([tweet], destination=str(tmp_path))
    extract_text(str(tmp_path))
    with open(f"{tmp_path}.json") as fp:
        ocr_texts = json.load(fp)
    ocr_text = " ".join(text.strip() for text in ocr_texts.get(tweet["id"], []))
    shutil.rmtree(tmp_path)

    return detect_scam(f"{text} {ocr_text}".strip())
