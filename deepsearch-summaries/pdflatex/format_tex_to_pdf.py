#!/usr/bin/env python3
"""
Script simple pour formatter les fichiers .tex en PDF
Utilise pdflatex pour compiler tous les fichiers .tex du répertoire courant
"""

import os
import subprocess
import sys

def compile_tex_to_pdf(tex_file):
    """Compile un fichier .tex en PDF avec pdflatex"""
    print(f"Compilation de {tex_file}...")
    
    try:
        # Exécuter pdflatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=os.path.dirname(os.path.abspath(tex_file)) or "."
        )
        
        if result.returncode == 0:
            print(f"✅ {tex_file} compilé avec succès!")
            return True
        else:
            print(f"❌ Erreur lors de la compilation de {tex_file}")
            print("Détails de l'erreur:")
            print(result.stdout)
            print(result.stderr)
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
    
    print(f"Fichiers .tex trouvés: {len(tex_files)}")
    for tex_file in tex_files:
        print(f"  - {os.path.basename(tex_file)}")
    
    print("\n" + "="*50)
    
    # Compiler chaque fichier
    success_count = 0
    for tex_file in tex_files:
        if compile_tex_to_pdf(tex_file):
            success_count += 1
        print("-" * 30)
    
    print(f"\nRésumé: {success_count}/{len(tex_files)} fichiers compilés avec succès")
    
    # Nettoyer les fichiers auxiliaires (optionnel)
    cleanup = input("\nVoulez-vous nettoyer les fichiers auxiliaires (.aux, .log, etc.)? (y/N): ")
    if cleanup.lower() in ['y', 'yes', 'o', 'oui']:
        cleanup_aux_files(current_dir)

def cleanup_aux_files(directory):
    """Nettoie les fichiers auxiliaires créés par LaTeX"""
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm', '.vrb']
    
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in aux_extensions):
            try:
                os.remove(os.path.join(directory, file))
                print(f"Supprimé: {file}")
            except OSError as e:
                print(f"Erreur lors de la suppression de {file}: {e}")

if __name__ == "__main__":
    main()
