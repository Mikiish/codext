#!/bin/bash

echo "Installation des dépendances LaTeX et Pandoc..."

# Update and upgrade the system
echo "Mise à jour et mise à niveau du système..."
sudo apt update -y -qq && sudo apt upgrade -y -qq
# Install Pandoc and LaTeX dependencies
echo "Installation de Pandoc et des dépendances LaTeX..."
sudo apt install -y pandoc
sudo apt install -y texlive-latex-base texlive-latex-extra texlive-lang-french

echo "Installation terminée !"
