#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fichier principal de lancement
Plateforme Intelligente d'Analyse et d'Amélioration d'Images
Conforme au cahier des charges du Sujet 1 - Architecture Modulaire
"""

import sys
import os

# Ajouter le répertoire courant au chemin Python pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.interface import main

if __name__ == "__main__":
    
    print(" Lancement de la Plateforme Intelligente d'Analyse d'Images")
    print(" Architecture modulaire conforme au cahier des charges du Sujet 1")
    print(" Modules chargés: interface, image_processor, visualization")
    print(" Ouverture de l'interface Streamlit...")
    
    # Lancer l'interface principale
    main()
