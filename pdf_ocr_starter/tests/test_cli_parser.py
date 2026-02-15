from pathlib import Path

from ocr_pdf.cli import build_parser


def test_parser_minimal_args() -> None:
    parser = build_parser()
    args = parser.parse_args(["--input", "a.pdf", "--output", "out.txt"])
    assert args.input == Path("a.pdf")
    assert args.output == Path("out.txt")
    assert args.lang == "eng"
    assert args.dpi == 300
