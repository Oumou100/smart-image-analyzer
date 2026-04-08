#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de visualisation
Contient toutes les fonctions pour l'affichage des histogrammes et comparaisons
Conforme au cahier des charges du Sujet 1
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Visualizer:
    """
    Classe pour la visualisation des images et histogrammes
    Contient toutes les méthodes d'affichage demandées dans le cahier des charges
    """
    
    @staticmethod
    def convert_bgr_to_rgb(image):
        """
        Convertir une image BGR (OpenCV) en RGB (matplotlib)
        
        Args:
            image: Image OpenCV en BGR
            
        Returns:
            Image RGB
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    @staticmethod
    def create_histogram(image, bins=256):
        """
        Créer un histogramme pour une image
        
        Args:
            image: Image à analyser
            bins: Nombre de bins pour l'histogramme
            
        Returns:
            tuple: (histogrammes, couleurs)
        """
        histograms = []
        colors = []
        
        if len(image.shape) == 3:
            # Image couleur - histogrammes RGB
            colors = ['b', 'g', 'r']
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [bins], [0, 256])
                histograms.append(hist)
        else:
            # Image niveaux de gris
            colors = ['black']
            hist = cv2.calcHist([image], [0], None, [bins], [0, 256])
            histograms.append(hist)
            
        return histograms, colors
    
    @staticmethod
    def plot_histogram(image, title="Histogramme", figsize=(10, 6)):
        """
        Créer et afficher un histogramme
        
        Args:
            image: Image à analyser
            title: Titre du graphique
            figsize: Taille de la figure
            
        Returns:
            matplotlib.figure.Figure: Figure matplotlib
        """
        histograms, colors = Visualizer.create_histogram(image)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for i, (hist, color) in enumerate(zip(histograms, colors)):
            ax.plot(hist, color=color, alpha=0.7, 
                   label=['Bleu', 'Vert', 'Rouge', 'Niveaux de gris'][i])
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Intensité', fontsize=12)
        ax.set_ylabel('Fréquence', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_comparison_histograms(original_image, processed_image, 
                                 figsize=(15, 5)):
        """
        Créer une comparaison d'histogrammes avant/après
        
        Args:
            original_image: Image originale
            processed_image: Image traitée
            figsize: Taille de la figure
            
        Returns:
            matplotlib.figure.Figure: Figure matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histogramme original
        histograms_orig, colors_orig = Visualizer.create_histogram(original_image)
        for i, (hist, color) in enumerate(zip(histograms_orig, colors_orig)):
            ax1.plot(hist, color=color, alpha=0.7)
        
        ax1.set_title('Histogramme Original', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Intensité', fontsize=10)
        ax1.set_ylabel('Fréquence', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Légende pour l'original
        if len(original_image.shape) == 3:
            ax1.legend(['Bleu', 'Vert', 'Rouge'])
        
        # Histogramme traité
        histograms_proc, colors_proc = Visualizer.create_histogram(processed_image)
        for i, (hist, color) in enumerate(zip(histograms_proc, colors_proc)):
            ax2.plot(hist, color=color, alpha=0.7)
        
        ax2.set_title('Histogramme Traité', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Intensité', fontsize=10)
        ax2.set_ylabel('Fréquence', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Légende pour le traité
        if len(processed_image.shape) == 3:
            ax2.legend(['Bleu', 'Vert', 'Rouge'])
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_side_by_side(original_image, processed_image, 
                         original_title="Image Originale", 
                         processed_title="Image Traitée",
                         figsize=(15, 6)):
        """
        Afficher deux images côte à côte
        
        Args:
            original_image: Image originale
            processed_image: Image traitée
            original_title: Titre pour l'image originale
            processed_title: Titre pour l'image traitée
            figsize: Taille de la figure
            
        Returns:
            matplotlib.figure.Figure: Figure matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Convertir en RGB pour matplotlib
        orig_rgb = Visualizer.convert_bgr_to_rgb(original_image)
        proc_rgb = Visualizer.convert_bgr_to_rgb(processed_image)
        
        # Afficher les images
        ax1.imshow(orig_rgb)
        ax1.set_title(original_title, fontsize=12, fontweight='bold')
        ax1.axis('off')
        
        ax2.imshow(proc_rgb)
        ax2.set_title(processed_title, fontsize=12, fontweight='bold')
        ax2.axis('off')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_statistics_comparison(original_stats, processed_stats, 
                                  figsize=(12, 6)):
        """
        Comparer les statistiques de deux images
        
        Args:
            original_stats: Statistiques de l'image originale
            processed_stats: Statistiques de l'image traitée
            figsize: Taille de la figure
            
        Returns:
            matplotlib.figure.Figure: Figure matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Données pour les graphiques
        labels = ['Moyenne', 'Écart-type', 'Min', 'Max']
        original_values = [
            original_stats.get('mean', 0),
            original_stats.get('std', 0),
            original_stats.get('min', 0),
            original_stats.get('max', 0)
        ]
        processed_values = [
            processed_stats.get('mean', 0),
            processed_stats.get('std', 0),
            processed_stats.get('min', 0),
            processed_stats.get('max', 0)
        ]
        
        # Graphique en barres pour la moyenne
        x = np.arange(len(labels))
        width = 0.35
        
        ax1.bar(x - width/2, original_values, width, label='Original', alpha=0.7)
        ax1.bar(x + width/2, processed_values, width, label='Traité', alpha=0.7)
        
        ax1.set_title('Comparaison des Statistiques', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Valeur', fontsize=10)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for i, (orig_val, proc_val) in enumerate(zip(original_values, processed_values)):
            ax1.text(i - width/2, orig_val + 1, f'{orig_val:.1f}', 
                    ha='center', va='bottom', fontsize=8)
            ax1.text(i + width/2, proc_val + 1, f'{proc_val:.1f}', 
                    ha='center', va='bottom', fontsize=8)
        
        # Graphique pour les dimensions
        ax2.text(0.1, 0.8, f'Original: {original_stats.get("shape", "N/A")}', 
                transform=ax2.transAxes, fontsize=10, fontweight='bold')
        ax2.text(0.1, 0.6, f'Traité: {processed_stats.get("shape", "N/A")}', 
                transform=ax2.transAxes, fontsize=10, fontweight='bold')
        ax2.text(0.1, 0.4, f'Canaux Original: {original_stats.get("channels", "N/A")}', 
                transform=ax2.transAxes, fontsize=10)
        ax2.text(0.1, 0.2, f'Canaux Traité: {processed_stats.get("channels", "N/A")}', 
                transform=ax2.transAxes, fontsize=10)
        
        ax2.set_title('Informations sur les Images', fontsize=12, fontweight='bold')
        ax2.axis('off')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_treatment_summary(original_image, processed_image, 
                               treatment_history, original_stats, processed_stats):
        """
        Créer une fiche récapitulative du traitement
        
        Args:
            original_image: Image originale
            processed_image: Image traitée
            treatment_history: Historique des traitements
            original_stats: Statistiques originales
            processed_stats: Statistiques traitées
            
        Returns:
            matplotlib.figure.Figure: Figure matplotlib
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Grille pour l'affichage
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Images côte à côte
        ax1 = fig.add_subplot(gs[0, :2])
        orig_rgb = Visualizer.convert_bgr_to_rgb(original_image)
        proc_rgb = Visualizer.convert_bgr_to_rgb(processed_image)
        
        # Afficher les images côte à côte
        combined = np.hstack([orig_rgb, proc_rgb])
        ax1.imshow(combined)
        ax1.set_title('Comparaison Avant/Après', fontsize=14, fontweight='bold')
        ax1.axis('off')
        
        # Informations sur les images
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.axis('off')
        
        info_text = f"""INFORMATIONS
        
Original:
{original_stats.get('shape', 'N/A')}
Canaux: {original_stats.get('channels', 'N/A')}
Moyenne: {original_stats.get('mean', 0):.1f}
Écart-type: {original_stats.get('std', 0):.1f}

Traité:
{processed_stats.get('shape', 'N/A')}
Canaux: {processed_stats.get('channels', 'N/A')}
Moyenne: {processed_stats.get('mean', 0):.1f}
Écart-type: {processed_stats.get('std', 0):.1f}
"""
        
        ax2.text(0.1, 0.5, info_text, transform=ax2.transAxes, 
                fontsize=10, verticalalignment='center', fontfamily='monospace')
        ax2.set_title('Statistiques', fontsize=12, fontweight='bold')
        
        # Histogrammes comparatifs
        ax3 = fig.add_subplot(gs[1, :])
        histograms_orig, colors_orig = Visualizer.create_histogram(original_image)
        histograms_proc, colors_proc = Visualizer.create_histogram(processed_image)
        
        for i, (hist_orig, hist_proc, color) in enumerate(zip(histograms_orig, histograms_proc, colors_orig)):
            ax3.plot(hist_orig, color=color, alpha=0.5, linestyle='-', 
                    label=['Bleu Orig', 'Vert Orig', 'Rouge Orig', 'Gris Orig'][i])
            ax3.plot(hist_proc, color=color, alpha=0.8, linestyle='--', 
                    label=['Bleu Traité', 'Vert Traité', 'Rouge Traité', 'Gris Traité'][i])
        
        ax3.set_title('Histogrammes Comparatifs', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Intensité', fontsize=10)
        ax3.set_ylabel('Fréquence', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=8)
        
        # Historique des traitements
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')
        
        history_text = "HISTORIQUE DES TRAITEMENTS:\n" + "\n".join(
            [f"• {treatment}" for treatment in treatment_history[-10:]]
        )
        
        ax4.text(0.05, 0.95, history_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        ax4.set_title('Historique des Traitements', fontsize=12, fontweight='bold')
        
        plt.suptitle('FICHE RECAPITULATIVE DE TRAITEMENT', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        return fig
    
    @staticmethod
    def convert_to_pil(image):
        """
        Convertir une image OpenCV en PIL Image
        
        Args:
            image: Image OpenCV
            
        Returns:
            PIL.Image: Image PIL
        """
        rgb_image = Visualizer.convert_bgr_to_rgb(image)
        return Image.fromarray(rgb_image)
    
    @staticmethod
    def save_figure(fig, filename, dpi=300):
        """
        Sauvegarder une figure matplotlib
        
        Args:
            fig: Figure matplotlib
            filename: Nom du fichier de sortie
            dpi: Résolution de l'image
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
