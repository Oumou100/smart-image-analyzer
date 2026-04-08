#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package modules pour l'architecture modulaire
Contient les modules conformes au cahier des charges du Sujet 1
"""

__version__ = "1.0.0"
__author__ = "Smart Image Analyzer Team"
__description__ = "Plateforme Intelligente d'Analyse et d'Amélioration d'Images"

# Modules disponibles
from .image_processor import ImageProcessor
from .visualization import Visualizer
from .interface import StreamlitInterface

__all__ = [
    'ImageProcessor',
    'Visualizer', 
    'StreamlitInterface'
]
