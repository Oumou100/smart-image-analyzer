#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de traitement d'images
Contient toutes les fonctions OpenCV pour le traitement d'images
Conforme au cahier des charges du Sujet 1
"""

import cv2
import numpy as np

class ImageProcessor:
    """
    Classe principale pour le traitement d'images
    Contient toutes les méthodes de traitement demandées dans le cahier des charges
    """
    
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.treatment_history = []
    
    def load_image(self, image_data):
        """
        Charger une image depuis des données binaires
        
        Args:
            image_data: Données binaires de l'image
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Convertir les données en image OpenCV
            nparr = np.frombuffer(image_data, np.uint8)
            self.original_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if self.original_image is None:
                return False
                
            self.processed_image = self.original_image.copy()
            self.treatment_history = ["Image chargée"]
            return True
            
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return False
    
    def reset_image(self):
        """Réinitialiser l'image à son état original"""
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.treatment_history.append("Réinitialisation")
    
    # ==========================================
    # AJUSTEMENTS PHOTOMETRIQUES
    # ==========================================
    
    def adjust_brightness_contrast(self, brightness=0, contrast=1.0):
        """
        Ajuster la luminosité et le contraste
        
        Args:
            brightness: Valeur de luminosité (-100 à +100)
            contrast: Facteur de contraste (0.1 à 3.0)
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        result = cv2.convertScaleAbs(self.original_image, alpha=contrast, beta=brightness)
        self.processed_image = result
        self.treatment_history.append(f"Luminosité: {brightness}, Contraste: {contrast}")
        return result
    
    def adjust_gamma(self, gamma=1.0):
        """
        Ajuster le gamma de l'image
        
        Args:
            gamma: Valeur gamma (0.1 à 3.0)
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        result = cv2.LUT(self.original_image, table)
        self.processed_image = result
        self.treatment_history.append(f"Gamma: {gamma}")
        return result
    
    # ==========================================
    # FILTRES SPATIAUX
    # ==========================================
    
    def apply_gaussian_blur(self, kernel_size=5):
        """
        Appliquer un filtre gaussien
        
        Args:
            kernel_size: Taille du noyau (doit être impair)
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        if kernel_size % 2 == 0:
            kernel_size += 1  # Assurer un noyau impair
            
        result = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
        self.processed_image = result
        self.treatment_history.append(f"Filtre gaussien: {kernel_size}x{kernel_size}")
        return result
    
    def apply_median_filter(self, kernel_size=5):
        """
        Appliquer un filtre médian
        
        Args:
            kernel_size: Taille du noyau (doit être impair)
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        if kernel_size % 2 == 0:
            kernel_size += 1  # Assurer un noyau impair
            
        result = cv2.medianBlur(self.original_image, kernel_size)
        self.processed_image = result
        self.treatment_history.append(f"Filtre médian: {kernel_size}x{kernel_size}")
        return result
    
    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):
        """
        Appliquer un filtre bilatéral
        
        Args:
            d: Diamètre du voisinage
            sigma_color: Écart-type pour l'espace couleur
            sigma_space: Écart-type pour l'espace spatial
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        result = cv2.bilateralFilter(self.original_image, d, sigma_color, sigma_space)
        self.processed_image = result
        self.treatment_history.append(f"Filtre bilatéral: d={d}")
        return result
    
    def apply_sharpening(self):
        """
        Appliquer un filtre de netteté (sharpening)
        
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        result = cv2.filter2D(self.original_image, -1, kernel)
        self.processed_image = result
        self.treatment_history.append("Filtre de netteté")
        return result
    
    # ==========================================
    # SEUILLAGE
    # ==========================================
    
    def apply_threshold_manual(self, threshold_value=127):
        """
        Appliquer un seuillage manuel
        
        Args:
            threshold_value: Valeur de seuil (0-255)
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        self.treatment_history.append(f"Seuillage manuel: {threshold_value}")
        return result
    
    def apply_threshold_otsu(self):
        """
        Appliquer un seuillage automatique avec la méthode d'Otsu
        
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        self.treatment_history.append("Seuillage Otsu")
        return result
    
    def apply_adaptive_threshold(self, method='mean'):
        """
        Appliquer un seuillage adaptatif
        
        Args:
            method: 'mean' pour moyenne, 'gaussian' pour gaussien
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        if method == 'mean':
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            self.treatment_history.append("Seuillage adaptatif moyen")
        else:
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            self.treatment_history.append("Seuillage adaptatif gaussien")
            
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        return result
    
    # ==========================================
    # EGALISATION D'HISTOGRAMME
    # ==========================================
    
    def equalize_histogram_global(self):
        """
        Appliquer une égalisation d'histogramme globale
        
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        if len(self.original_image.shape) == 3:
            yuv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2YUV)
            yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
            result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        else:
            result = cv2.equalizeHist(self.original_image)
            
        self.processed_image = result
        self.treatment_history.append("Égalisation histogramme globale")
        return result
    
    def equalize_histogram_clahe(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        """
        Appliquer une égalisation d'histogramme CLAHE
        
        Args:
            clip_limit: Limite de contraste
            tile_grid_size: Taille de la grille
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        
        if len(self.original_image.shape) == 3:
            yuv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2YUV)
            yuv[:,:,0] = clahe.apply(yuv[:,:,0])
            result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        else:
            result = clahe.apply(self.original_image)
            
        self.processed_image = result
        self.treatment_history.append("Égalisation CLAHE")
        return result
    
    # ==========================================
    # OPERATIONS MORPHOLOGIQUES
    # ==========================================
    
    def apply_morphology(self, operation, kernel_size=5):
        """
        Appliquer une opération morphologique
        
        Args:
            operation: 'erosion', 'dilation', 'opening', 'closing'
            kernel_size: Taille du noyau
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        if operation == 'erosion':
            result = cv2.erode(self.original_image, kernel, iterations=1)
            self.treatment_history.append(f"Érosion: {kernel_size}x{kernel_size}")
        elif operation == 'dilation':
            result = cv2.dilate(self.original_image, kernel, iterations=1)
            self.treatment_history.append(f"Dilatation: {kernel_size}x{kernel_size}")
        elif operation == 'opening':
            result = cv2.morphologyEx(self.original_image, cv2.MORPH_OPEN, kernel)
            self.treatment_history.append(f"Ouverture: {kernel_size}x{kernel_size}")
        elif operation == 'closing':
            result = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)
            self.treatment_history.append(f"Fermeture: {kernel_size}x{kernel_size}")
        else:
            return None
            
        self.processed_image = result
        return result
    
    # ==========================================
    # DETECTION DE CONTOURS
    # ==========================================
    
    def detect_edges_canny(self, low_threshold=50, high_threshold=150):
        """
        Détecter les contours avec l'algorithme de Canny
        
        Args:
            low_threshold: Seuil bas
            high_threshold: Seuil haut
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        self.treatment_history.append(f"Contours Canny: {low_threshold}-{high_threshold}")
        return result
    
    def detect_edges_sobel(self):
        """
        Détecter les contours avec l'algorithme de Sobel
        
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
        result = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        self.treatment_history.append("Contours Sobel")
        return result
    
    def detect_edges_laplacian(self):
        """
        Détecter les contours avec l'algorithme Laplacien
        
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        # Convertir en niveaux de gris
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.original_image
            
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.absolute(laplacian)
        laplacian = np.clip(laplacian, 0, 255).astype(np.uint8)
        result = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
        self.processed_image = result
        self.treatment_history.append("Contours Laplacien")
        return result
    
    # ==========================================
    # TRANSFORMATIONS GEOMETRIQUES
    # ==========================================
    
    def rotate_image(self, angle):
        """
        Rotater l'image
        
        Args:
            angle: Angle de rotation en degrés
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        h, w = self.original_image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        result = cv2.warpAffine(self.original_image, matrix, (w, h))
        self.processed_image = result
        self.treatment_history.append(f"Rotation: {angle}°")
        return result
    
    def flip_image(self, flip_code):
        """
        Retourner l'image
        
        Args:
            flip_code: 0 pour vertical, 1 pour horizontal, -1 pour les deux
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        result = cv2.flip(self.original_image, flip_code)
        self.processed_image = result
        
        if flip_code == 0:
            self.treatment_history.append("Flip vertical")
        elif flip_code == 1:
            self.treatment_history.append("Flip horizontal")
        else:
            self.treatment_history.append("Flip both")
            
        return result
    
    def resize_image(self, width, height):
        """
        Redimensionner l'image
        
        Args:
            width: Nouvelle largeur
            height: Nouvelle hauteur
            
        Returns:
            Image traitée
        """
        if self.original_image is None:
            return None
            
        result = cv2.resize(self.original_image, (width, height))
        self.processed_image = result
        self.treatment_history.append(f"Redimensionnement: {width}x{height}")
        return result
    
    # ==========================================
    # UTILITAIRES
    # ==========================================
    
    def get_image_stats(self, image=None):
        """
        Obtenir les statistiques d'une image
        
        Args:
            image: Image à analyser (None pour l'image actuelle)
            
        Returns:
            dict: Statistiques de l'image
        """
        if image is None:
            image = self.processed_image
            
        if image is None:
            return {}
            
        # Convertir en niveaux de gris si nécessaire
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        stats = {
            'mean': np.mean(gray),
            'std': np.std(gray),
            'min': np.min(gray),
            'max': np.max(gray),
            'shape': image.shape,
            'channels': image.shape[2] if len(image.shape) == 3 else 1
        }
        
        return stats
    
    def get_treatment_history(self):
        """
        Obtenir l'historique des traitements appliqués
        
        Returns:
            list: Historique des traitements
        """
        return self.treatment_history.copy()
    
    def save_image(self, filename):
        """
        Sauvegarder l'image traitée
        
        Args:
            filename: Nom du fichier de sortie
            
        Returns:
            bool: True si succès, False sinon
        """
        if self.processed_image is None:
            return False
            
        try:
            return cv2.imwrite(filename, self.processed_image)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
