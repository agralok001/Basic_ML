from __future__ import annotations

import argparse
from pathlib import Path

from .config import OCRConfig
from .pipeline import extract_pdf_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files with OCR fallback."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input PDF path")
    parser.add_argument("--output", required=True, type=Path, help="Output text path")
    parser.add_argument("--meta", type=Path, default=None, help="Optional JSON metadata output")
    parser.add_argument("--lang", default="eng", help="OCR language, e.g. eng, deu, fra")
    parser.add_argument("--dpi", type=int, default=300, help="Rasterization DPI for OCR")
    parser.add_argument("--force-ocr", action="store_true", help="Run OCR for all pages")
    parser.add_argument(
        "--min-text-chars",
        type=int,
        default=25,
        help="Use OCR when text-layer chars are below this threshold",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input PDF not found: {args.input}")
    if args.input.suffix.lower() != ".pdf":
        raise ValueError(f"Input must be a PDF file: {args.input}")

    config = OCRConfig(
        input_pdf=args.input,
        output_txt=args.output,
        output_meta_json=args.meta,
        lang=args.lang,
        dpi=args.dpi,
        force_ocr=args.force_ocr,
        min_text_chars=args.min_text_chars,
    )
    result = extract_pdf_text(config)
    print(f"Processed {len(result.pages)} pages.")
    print(f"Text output: {args.output}")
    if args.meta:
        print(f"Metadata output: {args.meta}")


if __name__ == "__main__":
    main()
