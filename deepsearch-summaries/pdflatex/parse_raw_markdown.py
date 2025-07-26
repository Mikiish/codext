#!/usr/bin/env python3
"""
Parser intelligent pour convertir raw.md en LaTeX propre
Gère les formules échappées et autres patterns LaTeX
"""

import re
import os

def parse_latex_from_markdown(input_file, output_file):
    """Parse un fichier markdown avec du LaTeX échappé et génère un .tex propre"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 Lecture de {input_file}...")
    
    # 1. Convertir les formules LaTeX échappées \$...\$ en $...$
    content = re.sub(r'\\(\$[^$]*?\$)', r'\1', content)
    print("✅ Formules LaTeX \\$...\\$ → $...$")
    
    # 2. Corriger les underscores échappés dans les formules mathématiques
    # Pattern pour trouver les formules et corriger les \_ dedans
    def fix_underscores_in_math(match):
        formula = match.group(1)
        # Dans les formules math, on veut _ et pas \_
        formula = formula.replace(r'\_', '_')
        return f"${formula}$"
    
    content = re.sub(r'\$([^$]*?)\$', fix_underscores_in_math, content)
    print("✅ Underscores corrigés dans les formules")
    
    # 3. Extraire le titre AVANT de convertir les titres
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        doc_title = title_match.group(1)
        print(f"📊 Titre trouvé: {doc_title}")
    else:
        doc_title = "Synthèse sur nombres premiers, flottants, p-adiques, théorie de Galois et calcul parallèle"
        print(f"📊 Titre par défaut: {doc_title}")
    
    # 4. Nettoyer le début du fichier (avant le premier titre)
    # Trouver le premier titre et commencer à partir de là
    if title_match:
        title_pos = content.find(title_match.group(0))
        if title_pos > 0:
            # Garder tout à partir du premier titre
            content = content[title_pos:]
        # Enlever le titre principal du contenu (il sera dans \title)
        content = re.sub(r'^# .+?\n', '', content, count=1, flags=re.MULTILINE)
    
    # 5. Gérer les titres markdown → LaTeX sections
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
    print("✅ Titres markdown → sections LaTeX")
    
    # 6. Convertir le gras **texte** en \\textbf{texte}
    content = re.sub(r'\*\*([^*]+?)\*\*', r'\\textbf{\1}', content)
    print("✅ Gras **texte** → \\\\textbf{texte}")
    
    # 7. Convertir l'italique *texte* en \\textit{texte} (attention aux formules)
    # On évite de toucher aux formules math
    def fix_italic(match):
        text = match.group(1)
        # Si c'est une formule math, on ne touche pas
        if '$' in text or '\\' in text:
            return f"*{text}*"
        return f"\\textit{{{text}}}"
    
    content = re.sub(r'\*([^*]+?)\*', fix_italic, content)
    print("✅ Italique *texte* → \\\\textit{texte}")
    
    # 8. Nettoyer les espaces multiples et lignes vides excessives
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r' +', ' ', content)
    print("✅ Espaces et lignes nettoyés")
    
    # 9. Créer le document LaTeX complet
    latex_template = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[french]{{babel}}
\\usepackage{{amsmath,amsfonts,amssymb}}
\\usepackage{{geometry}}
\\usepackage{{url}}
\\usepackage{{hyperref}}
\\usepackage{{enumitem}}

\\geometry{{margin=2.5cm}}

\\title{{{doc_title}}}
\\author{{Généré automatiquement depuis raw.md}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle
\\tableofcontents
\\newpage

{content.strip()}

\\end{{document}}"""

    # 10. Sauvegarder
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_template)
    
    print(f"✅ Document LaTeX généré: {output_file}")
    print(f"📊 Titre: {doc_title}")
    
    return output_file

def main():
    """Fonction principale"""
    input_file = "raw.md"
    output_file = "raw_parsed.tex"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier {input_file} introuvable!")
        return
    
    print("🚀 Parsing intelligent de raw.md...")
    print("="*60)
    
    try:
        parsed_file = parse_latex_from_markdown(input_file, output_file)
        
        print("="*60)
        print(f"🎉 Parsing terminé avec succès!")
        print(f"📁 Fichier généré: {parsed_file}")
        
        # Option pour compiler directement
        compile_choice = input("\n💡 Voulez-vous compiler en PDF maintenant? (y/N): ")
        if compile_choice.lower() in ['y', 'yes', 'o', 'oui']:
            compile_to_pdf(parsed_file)
            
    except Exception as e:
        print(f"❌ Erreur lors du parsing: {e}")

def compile_to_pdf(tex_file):
    """Compile le fichier tex en PDF"""
    import subprocess
    
    print(f"\n📄 Compilation de {tex_file}...")
    
    try:
        # Compiler deux fois pour les références
        for i in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
        
        pdf_file = tex_file.replace('.tex', '.pdf')
        if os.path.exists(pdf_file):
            print(f"✅ PDF généré: {pdf_file}")
        else:
            print(f"❌ Échec de compilation")
            print("Premières lignes d'erreur:")
            print(result.stdout.split('\n')[:10])
            
    except FileNotFoundError:
        print("❌ pdflatex non trouvé. Installez texlive-latex-extra")

if __name__ == "__main__":
    main()
