# PDF OCR Starter Module

This module provides a structured Python starter project to extract text from PDF files using:

- direct text extraction for text-based PDFs
- OCR fallback for scanned/image-only pages

## Features

- clean package layout (`ocr_pdf/`)
- CLI entry point
- page-level OCR with configurable language and DPI
- JSON metadata output

## Requirements

1. Python 3.10+
2. Tesseract OCR installed and available in `PATH`

On Windows, install Tesseract and ensure `tesseract.exe` is in your system `PATH`.

## Install

```bash
cd pdf_ocr_starter
pip install -r requirements.txt
```

## Usage

```bash
python -m ocr_pdf.cli --input "sample.pdf" --output "output.txt"
```

With metadata JSON:

```bash
python -m ocr_pdf.cli --input "sample.pdf" --output "output.txt" --meta "output_meta.json"
```

Force OCR for every page:

```bash
python -m ocr_pdf.cli --input "sample.pdf" --output "output.txt" --force-ocr
```

## Streamlit UI

Run a simple local UI:

```bash
streamlit run streamlit_app.py
```

UI capabilities:

- upload a PDF
- choose OCR language, DPI, and fallback threshold
- optionally force OCR on all pages
- preview extracted text
- download `.txt` and metadata `.json` outputs

## Notes

- If a page already has embedded text, the module uses that by default for speed.
- OCR is used only when needed, unless `--force-ocr` is enabled.
