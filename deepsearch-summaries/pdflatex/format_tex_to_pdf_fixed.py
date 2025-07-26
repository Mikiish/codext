#!/usr/bin/env python3
"""
Script pour convertir du texte brut en LaTeX et compiler en PDF
Ajoute automatiquement la structure LaTeX nécessaire
"""

import os
import subprocess
import sys

def text_to_latex(input_file, output_file):
    """Convertit un fichier texte en document LaTeX valide"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Template LaTeX basique
    latex_template = r"""\documentclass[12pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{amsmath,amsfonts,amssymb}}
\usepackage{{geometry}}
\usepackage{{url}}
\usepackage{{hyperref}}

\geometry{{margin=2.5cm}}

\title{{{title}}}
\author{{Document généré automatiquement}}
\date{{\today}}

\begin{{document}}

\maketitle

{content}

\end{{document}}
"""
    
    # Nettoyer le contenu pour LaTeX
    content_cleaned = content.replace('&', r'\&')
    content_cleaned = content_cleaned.replace('%', r'\%')
    content_cleaned = content_cleaned.replace('$', r'\$')
    content_cleaned = content_cleaned.replace('#', r'\#')
    content_cleaned = content_cleaned.replace('_', r'\_')
    content_cleaned = content_cleaned.replace('^', r'\^{}')
    content_cleaned = content_cleaned.replace('{', r'\{')
    content_cleaned = content_cleaned.replace('}', r'\}')
    
    # Remplacer les doubles retours à la ligne par des paragraphes
    content_cleaned = content_cleaned.replace('\n\n', '\n\n\\par\n')
    
    # Créer un titre basé sur le nom du fichier
    title = os.path.splitext(os.path.basename(input_file))[0].replace('_', ' ').replace('TEX ', '').title()
    
    # Générer le document LaTeX
    latex_content = latex_template.format(title=title, content=content_cleaned)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✅ Converti: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")

def compile_tex_to_pdf(tex_file):
    """Compile un fichier .tex en PDF avec pdflatex"""
    print(f"📄 Compilation de {os.path.basename(tex_file)}...")
    
    try:
        # Exécuter pdflatex deux fois pour les références croisées
        for i in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=os.path.dirname(os.path.abspath(tex_file)) or "."
            )
        
        if result.returncode == 0:
            pdf_name = os.path.splitext(tex_file)[0] + '.pdf'
            print(f"✅ {os.path.basename(tex_file)} compilé avec succès! -> {os.path.basename(pdf_name)}")
            return True
        else:
            print(f"❌ Erreur lors de la compilation de {os.path.basename(tex_file)}")
            # Afficher seulement les erreurs importantes
            if result.stderr:
                print("Erreurs:", result.stderr[:500])
            return False
            
    except FileNotFoundError:
        print("❌ pdflatex n'est pas installé ou introuvable dans le PATH")
        print("Installez-le avec: sudo apt install texlive-latex-base texlive-latex-extra")
        return False

def main():
    """Fonction principale"""
    current_dir = os.path.dirname(__file__)
    
    # Trouver tous les fichiers .tex
    tex_files = []
    for file in os.listdir(current_dir):
        if file.lower().endswith('.tex'):
            tex_files.append(os.path.join(current_dir, file))
    
    if not tex_files:
        print("Aucun fichier .tex trouvé dans le répertoire courant")
        return
    
    print(f"🔍 Fichiers .tex trouvés: {len(tex_files)}")
    for tex_file in tex_files:
        print(f"  - {os.path.basename(tex_file)}")
    
    print("\n" + "="*60)
    print("🔄 ÉTAPE 1: Conversion en LaTeX valide")
    print("="*60)
    
    # Convertir chaque fichier texte en LaTeX valide
    converted_files = []
    for tex_file in tex_files:
        base_name = os.path.splitext(tex_file)[0]
        latex_file = f"{base_name}_formatted.tex"
        text_to_latex(tex_file, latex_file)
        converted_files.append(latex_file)
    
    print("\n" + "="*60)
    print("📚 ÉTAPE 2: Compilation en PDF")
    print("="*60)
    
    # Compiler chaque fichier LaTeX
    success_count = 0
    for latex_file in converted_files:
        if compile_tex_to_pdf(latex_file):
            success_count += 1
        print("-" * 40)
    
    print(f"\n🎯 Résumé: {success_count}/{len(converted_files)} fichiers compilés avec succès")
    
    # Afficher les PDF générés
    pdf_files = []
    for latex_file in converted_files:
        pdf_file = os.path.splitext(latex_file)[0] + '.pdf'
        if os.path.exists(pdf_file):
            pdf_files.append(pdf_file)
    
    if pdf_files:
        print("\n📋 PDF générés:")
        for pdf_file in pdf_files:
            print(f"  ✅ {os.path.basename(pdf_file)}")
    
    # Nettoyer les fichiers auxiliaires (optionnel)
    cleanup = input("\n🧹 Voulez-vous nettoyer les fichiers auxiliaires (.aux, .log, etc.)? (y/N): ")
    if cleanup.lower() in ['y', 'yes', 'o', 'oui']:
        cleanup_aux_files(current_dir)

def cleanup_aux_files(directory):
    """Nettoie les fichiers auxiliaires créés par LaTeX"""
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm', '.vrb']
    
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in aux_extensions):
            try:
                os.remove(os.path.join(directory, file))
                print(f"🗑️  Supprimé: {file}")
            except OSError as e:
                print(f"❌ Erreur lors de la suppression de {file}: {e}")

if __name__ == "__main__":
    main()
