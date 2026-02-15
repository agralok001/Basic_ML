from __future__ import annotations

import io

import fitz
import pytesseract
from PIL import Image


def extract_text_layer(page: fitz.Page) -> str:
    """Extract embedded text from a PDF page."""
    return page.get_text("text").strip()


def ocr_page(page: fitz.Page, lang: str = "eng", dpi: int = 300) -> str:
    """Render a PDF page as an image and run OCR on it."""
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    image_bytes = pix.tobytes("png")
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image, lang=lang).strip()
