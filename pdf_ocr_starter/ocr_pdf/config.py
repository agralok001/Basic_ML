from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class OCRConfig:
    input_pdf: Path
    output_txt: Path
    output_meta_json: Path | None = None
    lang: str = "eng"
    dpi: int = 300
    force_ocr: bool = False
    min_text_chars: int = 25
