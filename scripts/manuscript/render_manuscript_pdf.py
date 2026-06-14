"""Render the generated DOCX to a review PDF through local HTML and Edge."""

from __future__ import annotations

import base64
import subprocess
from pathlib import Path

import mammoth

BASE_DIR = Path(__file__).resolve().parents[2]
DOCX_PATH = (
    BASE_DIR / "output" / "doc" / "ML4Africa_scientometric_manuscript.docx"
)
PDF_PATH = (
    BASE_DIR / "output" / "pdf" / "ML4Africa_scientometric_manuscript.pdf"
)
HTML_PATH = BASE_DIR / "tmp" / "docs" / "manuscript_render.html"
EDGE_PATHS = (
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
)

CSS = """
@page {
  size: Letter portrait;
  margin: 0.7in;
}
@page supplement {
  size: Letter landscape;
  margin: 0.55in;
}
html, body {
  color: #17324d;
  font-family: "Times New Roman", serif;
  font-size: 10.5pt;
  line-height: 1.24;
}
body {
  margin: 0;
}
h1, h2, h3 {
  color: #17324d;
  font-family: Arial, sans-serif;
  break-after: avoid-page;
}
h1 {
  font-size: 17pt;
  margin: 0 0 12pt;
}
h2 {
  border-bottom: 1px solid #d0d5dd;
  font-size: 14pt;
  margin: 13pt 0 6pt;
  padding-bottom: 2pt;
}
h3 {
  color: #0b7a75;
  font-size: 11.5pt;
  margin: 10pt 0 4pt;
}
p {
  margin: 0 0 6pt;
  orphans: 3;
  widows: 3;
}
a {
  color: #0b7a75;
}
img {
  display: block;
  height: auto;
  margin: 8pt auto 4pt;
  max-height: 8in;
  max-width: 100%;
  object-fit: contain;
}
table {
  border-collapse: collapse;
  font-family: Arial, sans-serif;
  font-size: 7.2pt;
  margin: 7pt 0 5pt;
  table-layout: auto;
  width: 100%;
}
th, td {
  border: 0.6pt solid #98a2b3;
  padding: 3pt;
  text-align: left;
  vertical-align: top;
  word-break: normal;
}
th {
  background: #17324d;
  color: white;
}
tr:nth-child(even) td {
  background: #eaf7f5;
}
ul, ol {
  margin: 4pt 0 7pt 20pt;
}
.supplement {
  page: supplement;
}
.supplement table {
  font-size: 6.2pt;
}
.supplement h1 {
  break-before: page;
}
h1 + p {
  margin-top: 0;
}
"""


def _image_converter(image):
    with image.open() as image_bytes:
        encoded = base64.b64encode(image_bytes.read()).decode("ascii")
    return {"src": f"data:{image.content_type};base64,{encoded}"}


def _build_html() -> str:
    with DOCX_PATH.open("rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file,
            convert_image=mammoth.images.img_element(_image_converter),
        )
    body = result.value
    supplement_heading = "<h1>Supplementary Material</h1>"
    if supplement_heading not in body:
        raise ValueError("Supplementary Material heading missing from DOCX conversion")
    body = body.replace(
        supplement_heading,
        f'<div class="supplement">{supplement_heading}',
        1,
    )
    body += "</div>"
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )


def render_pdf() -> Path:
    edge = next((path for path in EDGE_PATHS if path.exists()), None)
    if edge is None:
        raise FileNotFoundError("Microsoft Edge executable was not found")
    if not DOCX_PATH.exists():
        raise FileNotFoundError(DOCX_PATH)

    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(_build_html(), encoding="utf-8", newline="\n")

    command = [
        str(edge),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH.resolve().as_uri(),
    ]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0 or not PDF_PATH.exists():
        raise RuntimeError(
            "Edge PDF rendering failed: "
            f"code={result.returncode}; stderr={result.stderr.strip()}"
        )
    return PDF_PATH


def main() -> None:
    output = render_pdf()
    print(f"Review PDF built: {output}")


if __name__ == "__main__":
    main()
