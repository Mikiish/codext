#!/usr/bin/env python3
"""
Script pour convertir les fichiers .tex (texte brut) en vrais documents LaTeX puis en PDF
Utilise pdflatex avec support du français (babel-french)
"""

import os
import subprocess
import sys
import re

def convert_text_to_latex(text_file, output_tex):
    """Convertit un fichier texte en document LaTeX valide avec support français"""
    
    with open(text_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Nettoyer le contenu
    content = content.replace('TEX_', '')  # Supprimer le préfixe TEX_
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Réduire les sauts de ligne multiples
    content = content.strip()
    
    # Échapper seulement les caractères vraiment problématiques
    # On évite d'échapper $, ^, _, {, } car ils peuvent être des maths légitimes
    special_chars = {
        '%': r'\%',  # Commentaires LaTeX
        '#': r'\#',  # Paramètres de macro
    }
    
    for char, replacement in special_chars.items():
        content = content.replace(char, replacement)
    
    # Créer le document LaTeX
    latex_content = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[french]{{babel}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{geometry}}
\\geometry{{margin=2.5cm}}

\\title{{Document extrait}}
\\author{{Généré automatiquement}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

{content}

\\end{{document}}"""

    with open(output_tex, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✅ Fichier LaTeX créé: {output_tex}")

def compile_tex_to_pdf(tex_file):
    """Compile un fichier .tex en PDF avec pdflatex"""
    print(f"Compilation de {tex_file}...")
    
    try:
        # Exécuter pdflatex deux fois pour résoudre les références
        for i in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=os.path.dirname(os.path.abspath(tex_file)) or "."
            )
        
        # Vérifier si le PDF a été créé plutôt que le code de retour
        pdf_file = tex_file.replace('.tex', '.pdf')
        if os.path.exists(pdf_file):
            print(f"✅ {tex_file} compilé avec succès!")
            return True
        else:
            print(f"❌ Erreur lors de la compilation de {tex_file}")
            print("Premières lignes de l'erreur:")
            print(result.stdout.split('\n')[:10])
            return False
            
    except FileNotFoundError:
        print("❌ pdflatex n'est pas installé ou introuvable dans le PATH")
        print("Installez-le avec: sudo apt install texlive-latex-base texlive-latex-extra texlive-lang-french")
        return False

def main():
    """Fonction principale"""
    current_dir = os.path.dirname(__file__)
    
    # Trouver tous les fichiers .tex originaux (pas ceux déjà formatés)
    tex_files = []
    for file in os.listdir(current_dir):
        if file.lower().endswith('.tex') and '_formatted' not in file.lower():
            tex_files.append(os.path.join(current_dir, file))
    
    if not tex_files:
        print("Aucun fichier .tex trouvé dans le répertoire courant")
        return
    
    print(f"Fichiers .tex trouvés: {len(tex_files)}")
    for tex_file in tex_files:
        print(f"  - {os.path.basename(tex_file)}")
    
    print("\n" + "="*60)
    
    # Traiter chaque fichier
    success_count = 0
    for tex_file in tex_files:
        basename = os.path.splitext(os.path.basename(tex_file))[0]
        formatted_tex = os.path.join(current_dir, f"{basename}_formatted.tex")
        
        print(f"\n📄 Traitement de {os.path.basename(tex_file)}...")
        
        # Convertir le texte en LaTeX valide
        convert_text_to_latex(tex_file, formatted_tex)
        
        # Compiler en PDF
        if compile_tex_to_pdf(formatted_tex):
            success_count += 1
            print(f"📄➡️📋 {os.path.basename(tex_file)} → {basename}_formatted.pdf")
        
        print("-" * 40)
    
    print(f"\n🎉 Résumé: {success_count}/{len(tex_files)} fichiers traités avec succès")
    
    # Nettoyer les fichiers auxiliaires (optionnel)
    cleanup = input("\nVoulez-vous nettoyer les fichiers auxiliaires (.aux, .log, etc.)? (y/N): ")
    if cleanup.lower() in ['y', 'yes', 'o', 'oui']:
        cleanup_aux_files(current_dir)

def cleanup_aux_files(directory):
    """Nettoie les fichiers auxiliaires créés par LaTeX"""
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm', '.vrb']
    
    cleaned = 0
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in aux_extensions):
            try:
                os.remove(os.path.join(directory, file))
                print(f"🗑️ Supprimé: {file}")
                cleaned += 1
            except OSError as e:
                print(f"❌ Erreur lors de la suppression de {file}: {e}")
    
    if cleaned == 0:
        print("Aucun fichier auxiliaire à nettoyer")
    else:
        print(f"🧹 {cleaned} fichiers auxiliaires nettoyés")

if __name__ == "__main__":
    main()
