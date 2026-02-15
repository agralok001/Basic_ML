from __future__ import annotations

import json
from dataclasses import dataclass

import fitz

from .config import OCRConfig
from .extractor import extract_text_layer, ocr_page


@dataclass(slots=True)
class OCRPageResult:
    page_number: int
    mode: str
    text: str


@dataclass(slots=True)
class OCRPipelineResult:
    pages: list[OCRPageResult]

    @property
    def combined_text(self) -> str:
        return "\n\n".join(page.text for page in self.pages if page.text)


def extract_pdf_text(config: OCRConfig) -> OCRPipelineResult:
    doc = fitz.open(config.input_pdf)
    page_results: list[OCRPageResult] = []
    try:
        for page_index, page in enumerate(doc):
            text_layer = extract_text_layer(page)
            use_ocr = config.force_ocr or len(text_layer) < config.min_text_chars

            if use_ocr:
                page_text = ocr_page(page=page, lang=config.lang, dpi=config.dpi)
                mode = "ocr"
            else:
                page_text = text_layer
                mode = "text_layer"

            page_results.append(
                OCRPageResult(
                    page_number=page_index + 1,
                    mode=mode,
                    text=page_text,
                )
            )
    finally:
        doc.close()

    result = OCRPipelineResult(pages=page_results)
    config.output_txt.parent.mkdir(parents=True, exist_ok=True)
    config.output_txt.write_text(result.combined_text, encoding="utf-8")

    if config.output_meta_json:
        config.output_meta_json.parent.mkdir(parents=True, exist_ok=True)
        metadata = {
            "input_pdf": str(config.input_pdf),
            "output_txt": str(config.output_txt),
            "lang": config.lang,
            "dpi": config.dpi,
            "force_ocr": config.force_ocr,
            "pages": [
                {
                    "page_number": p.page_number,
                    "mode": p.mode,
                    "char_count": len(p.text),
                }
                for p in result.pages
            ],
        }
        config.output_meta_json.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

    return result
