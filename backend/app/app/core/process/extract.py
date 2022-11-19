import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

import requests
from tqdm import tqdm

from app.core.process.ocr.photo import ocr_photo
from app.core.process.ocr.video import ocr_video

VIDEO_FORMATS = ["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "m4v", "3gp", "3g2", "f4v", "f4p", "f4a", "f4b"]
PHOTO_FORMATS = ["jpg", "jpeg", "png", "bmp", "tiff", "tif"]


logger = logging.getLogger(__name__)


def ocr(file: str) -> str:
    """OCR file and return text."""
    suffix = Path(file).suffix[1:].lower()
    if suffix in VIDEO_FORMATS:
        return " ".join(ocr_video(file))
    elif suffix in PHOTO_FORMATS:
        return ocr_photo(file)
    else:
        logger.warning("Unsupported file format: %s", suffix)
        return ""


def download_media(tweets: List[Dict[str, Any]], destination: str, key: str = "media_url"):
    """Download media from given tweets to given destination directory."""
    for tweet in tweets:
        if tweet[key]:
            for idx, url in tqdm(enumerate(tweet[key]), desc="Downloading media"):
                filename = url.split("/")[-1]
                filename, suffix = filename.split(".")
                path = Path(destination) / f"{filename}_{idx}.{suffix}"
                if not path.exists():
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with path.open("wb") as fp:
                            for chunk in r.iter_content(chunk_size=8192):
                                fp.write(chunk)


def extract_text(directory: str):
    """Extract text from images and videos in given directory and save to json."""
    texts = defaultdict(list)
    for path in tqdm(Path(directory).iterdir(), desc="Extracting text"):
        id_, idx = path.stem.split("_")
        if path.is_file():
            text = ocr(str(path))
            texts[id_].append(text)
    with open(f"{directory}.json") as fp:
        json.dump(texts, fp)
