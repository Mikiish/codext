import os
import subprocess
import pdfplumber

PDF_DIR = os.path.dirname(__file__)


def extract_text_from_pdf(pdf_path, tex_path):
    with pdfplumber.open(pdf_path) as pdf, open(tex_path, "w", encoding="utf-8") as out:
        out.write("TEX_\n")
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                out.write(text + "\n")


def compile_tex_to_pdf(tex_path):
    # Compile .tex to .pdf using pdflatex
    subprocess.run(["pdflatex", tex_path], cwd=PDF_DIR)


def main():
    for fname in os.listdir(PDF_DIR):
        if fname.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, fname)
            tex_name = f"TEX_{os.path.splitext(fname)[0]}.tex"
            tex_path = os.path.join(PDF_DIR, tex_name)
            extract_text_from_pdf(pdf_path, tex_path)
            compile_tex_to_pdf(tex_name)
            print(f"PDF traité: {fname} -> {tex_name} -> PDF compilé")

if __name__ == "__main__":
    main()
