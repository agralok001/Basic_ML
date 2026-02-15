from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from ocr_pdf.config import OCRConfig
from ocr_pdf.pipeline import extract_pdf_text


def main() -> None:
    st.set_page_config(page_title="PDF OCR Starter", layout="wide")
    st.title("PDF OCR Starter")
    st.write("Upload a PDF and extract text with OCR fallback.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    col1, col2, col3 = st.columns(3)
    with col1:
        lang = st.text_input("OCR Language", value="eng", help="Tesseract language code")
    with col2:
        dpi = st.number_input("DPI", min_value=72, max_value=600, value=300, step=24)
    with col3:
        min_text_chars = st.number_input(
            "Min text chars",
            min_value=0,
            max_value=500,
            value=25,
            step=5,
            help="Use OCR when text layer is shorter than this value",
        )

    force_ocr = st.checkbox("Force OCR on all pages", value=False)

    if uploaded_pdf is None:
        return

    if st.button("Run OCR", type="primary"):
        with st.spinner("Running OCR..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                tmp = Path(temp_dir)
                input_pdf = tmp / uploaded_pdf.name
                output_txt = tmp / "output.txt"
                output_meta = tmp / "output_meta.json"

                input_pdf.write_bytes(uploaded_pdf.getvalue())

                config = OCRConfig(
                    input_pdf=input_pdf,
                    output_txt=output_txt,
                    output_meta_json=output_meta,
                    lang=lang.strip() or "eng",
                    dpi=int(dpi),
                    force_ocr=force_ocr,
                    min_text_chars=int(min_text_chars),
                )
                result = extract_pdf_text(config)

                text_value = output_txt.read_text(encoding="utf-8")
                meta_value = output_meta.read_text(encoding="utf-8")
                meta_data = json.loads(meta_value)

        st.success(f"Processed {len(result.pages)} pages.")

        st.subheader("Extracted Text")
        st.text_area("Text", value=text_value, height=360, label_visibility="collapsed")

        st.download_button(
            "Download Text (.txt)",
            data=text_value.encode("utf-8"),
            file_name=f"{Path(uploaded_pdf.name).stem}_ocr.txt",
            mime="text/plain",
        )
        st.download_button(
            "Download Metadata (.json)",
            data=meta_value.encode("utf-8"),
            file_name=f"{Path(uploaded_pdf.name).stem}_meta.json",
            mime="application/json",
        )

        st.subheader("Page Modes")
        st.dataframe(
            [
                {
                    "page_number": p["page_number"],
                    "mode": p["mode"],
                    "char_count": p["char_count"],
                }
                for p in meta_data["pages"]
            ],
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
