"""OCR toolkit.

A small, self-contained toolkit that ties together the four things explored in
the original scratch file into one coherent pipeline:

    image  ->  preprocess (OpenCV)  ->  OCR (pytesseract)  ->  parse fields (regex)

Sections
--------
1. Image preprocessing ....... grayscale, threshold, denoise, invert, morphology
2. OCR ....................... text extraction + orientation detection
3. Field parsing ............. pull name / email / phone out of raw OCR text
4. Regex reference ........... compact, runnable examples of the `re` module
5. CLI ....................... `python ocr_toolkit.py <image>`

Dependencies
------------
    pip install opencv-python pillow pytesseract numpy

The Tesseract *engine* must also be installed on the system (separate from the
Python wrapper). Point TESSERACT_CMD at it, or set the TESSERACT_CMD env var.
"""

from __future__ import annotations

import argparse
import os
import re
from typing import Optional

import cv2
import numpy as np
import pytesseract
from PIL import Image

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# On Windows this is typically r"C:\Program Files\Tesseract-OCR\tesseract.exe".
# On Linux/macOS the binary is usually already on PATH, so this can stay None.
TESSERACT_CMD: Optional[str] = os.environ.get("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


# ---------------------------------------------------------------------------
# 1. Image preprocessing
# ---------------------------------------------------------------------------

def read_image(path: str) -> np.ndarray:
    """Load an image from disk as a BGR OpenCV array."""
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path!r}")
    return image


def invert(image: np.ndarray) -> np.ndarray:
    """Invert colors (black <-> white). Useful for light-on-dark scans."""
    return cv2.bitwise_not(image)


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image to single-channel grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def binarize(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    """Convert to pure black-and-white using a fixed threshold.

    Expects a grayscale image. Pixels above `threshold` become white (255),
    the rest become black (0).
    """
    _, bw = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return bw


def remove_noise(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Smooth away speckle noise with a median blur."""
    return cv2.medianBlur(image, kernel_size)


def dilate(image: np.ndarray, kernel_size: int = 5, iterations: int = 1) -> np.ndarray:
    """Thicken strokes (grow white regions)."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)


def erode(image: np.ndarray, kernel_size: int = 5, iterations: int = 1) -> np.ndarray:
    """Thin strokes (shrink white regions)."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)


def preprocess(path: str, denoise: bool = True) -> np.ndarray:
    """Run a sensible default preprocessing pipeline for OCR.

    grayscale -> binarize -> (optional) denoise. Returns the cleaned image,
    which usually gives Tesseract a much easier time than the raw photo.
    """
    image = read_image(path)
    processed = binarize(to_grayscale(image))
    if denoise:
        processed = remove_noise(processed)
    return processed


# ---------------------------------------------------------------------------
# 2. OCR
# ---------------------------------------------------------------------------

def extract_text(image, lang: str = "eng", config: str = "--psm 6 --oem 3") -> str:
    """Run OCR on an image and return the recognized text.

    `image` may be a file path, a PIL Image, or an OpenCV/NumPy array.
    """
    if isinstance(image, str):
        image = Image.open(image)
    return pytesseract.image_to_string(image, lang=lang, config=config)


def detect_orientation(image) -> str:
    """Return Tesseract's orientation-and-script-detection (OSD) report."""
    return pytesseract.image_to_osd(image)


# ---------------------------------------------------------------------------
# 3. Field parsing (regex)
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{8,}\d")


def parse_contact_info(text: str) -> dict:
    """Extract a best-effort name / email / phone from raw OCR text.

    The name is a heuristic: the first non-empty line. Email and phone are
    matched with regex. Missing fields come back as empty strings.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    return {
        "name": lines[0] if lines else "",
        "email": emails[0] if emails else "",
        "phone": phones[0].strip() if phones else "",
    }


# ---------------------------------------------------------------------------
# 4. Regex reference (runnable examples of the `re` module)
# ---------------------------------------------------------------------------

def regex_examples() -> None:
    """Print a compact tour of the `re` functions from the original notes."""
    text = "The price is 45 dollars and 99 cents. Contact ID: 1290 today."

    # findall  -> every match as a list of strings
    print("findall  :", re.findall(r"\d+", text))

    # search   -> first match only, with .group()/.start()/.end()
    match = re.search(r"\d+", text)
    if match:
        print("search   :", match.group(), f"(index {match.start()}-{match.end()})")

    # finditer -> iterate over each match object
    print("finditer :", [(m.group(), m.start()) for m in re.finditer(r"\d+", text)])

    # groups   -> parentheses capture sub-parts of a match
    id_match = re.search(r"ID: (\d+)", text)
    if id_match:
        print("group(0) :", id_match.group(0))   # full match: "ID: 1290"
        print("group(1) :", id_match.group(1))   # captured:   "1290"

    # split    -> break a string on a pattern
    print("split    :", re.split(r"\W+", "Words, words, words."))

    # character classes: \w word chars, \W non-word chars
    print(r"\w+      :", re.findall(r"\w+", "he typed *** in some_language."))


# ---------------------------------------------------------------------------
# 5. CLI
# ---------------------------------------------------------------------------

def run(path: str, lang: str = "eng", show_osd: bool = False) -> dict:
    """Full pipeline for one image: preprocess -> OCR -> parse. Returns fields."""
    cleaned = preprocess(path)
    text = extract_text(cleaned, lang=lang)

    print("=" * 60)
    print("RAW TEXT")
    print("=" * 60)
    print(text.strip() or "(no text detected)")

    if show_osd:
        print("\nORIENTATION")
        print("-" * 60)
        print(detect_orientation(path).strip())

    fields = parse_contact_info(text)
    print("\nPARSED FIELDS")
    print("-" * 60)
    for key, value in fields.items():
        print(f"  {key:<6}: {value or '(none)'}")

    return fields


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preprocess an image, OCR it, and extract contact fields.",
    )
    parser.add_argument("image", nargs="?", help="path to the image file")
    parser.add_argument("--lang", default="eng", help="Tesseract language(s), e.g. eng+kan")
    parser.add_argument("--osd", action="store_true", help="also print orientation info")
    parser.add_argument("--demo", action="store_true", help="run the regex examples and exit")
    args = parser.parse_args()

    if args.demo:
        regex_examples()
        return

    if not args.image:
        parser.error("provide an image path, or pass --demo for the regex examples")

    run(args.image, lang=args.lang, show_osd=args.osd)


if __name__ == "__main__":
    main()