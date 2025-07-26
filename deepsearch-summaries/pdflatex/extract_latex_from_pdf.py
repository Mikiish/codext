import pdfplumber
import sys

if len(sys.argv) < 2:
    print("Usage: python extract_latex_from_pdf.py <pdf_path> [output_tex]")
    sys.exit(1)

pdf_path = sys.argv[1]
output_tex = sys.argv[2] if len(sys.argv) > 2 else "extrait_latex.tex"

with pdfplumber.open(pdf_path) as pdf, open(output_tex, "w", encoding="utf-8") as out:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            out.write(text + "\n")

print(f"Texte extrait dans {output_tex}")
