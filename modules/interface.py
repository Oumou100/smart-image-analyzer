
"""
Module d'interface utilisateur
Contient tous les widgets Streamlit pour l'interface graphique
"""

import streamlit as st
import numpy as np
import cv2
from modules.image_processor import ImageProcessor
from modules.visualization import Visualizer

class StreamlitInterface:
    """
    Classe principale pour l'interface Streamlit
    Contient tous les widgets et contrôles demandés dans le cahier des charges
    """
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.visualizer = Visualizer()
        
        # Initialiser l'état de la session
        if 'image_loaded' not in st.session_state:
            st.session_state.image_loaded = False
        if 'treatment_applied' not in st.session_state:
            st.session_state.treatment_applied = False
        if 'current_image' not in st.session_state:
            st.session_state.current_image = None
        if 'mode' not in st.session_state:
            st.session_state.mode = 'controlled'
        if 'saved_processed_image' not in st.session_state:
            st.session_state.saved_processed_image = None
    
    def setup_page(self):
        """Configurer la page Streamlit"""
        st.set_page_config(
            page_title="Smart Image Analyzer",
            page_icon="ressources/logo.png",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        
        st.title("Plateforme Intelligente d'Analyse et d'Amélioration d'Images")
    
    def create_sidebar(self):
        """
        Créer la barre latérale avec tous les contrôles
        
        Returns:
            dict: Paramètres sélectionnés par l'utilisateur
        """
        st.sidebar.header("Panneau de Contrôle")
        
        # Upload d'image
        uploaded_file = st.sidebar.file_uploader(
            "Charger une image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Supporte JPG, PNG, BMP, TIFF"
        )
        
        if uploaded_file is not None:
            # Charger l'image
            image_data = uploaded_file.read()
            if self.processor.load_image(image_data):
                st.session_state.image_loaded = True
                if self.processor.original_image is not None:
                    st.session_state.current_image = self.processor.original_image.copy()
                st.session_state.treatment_applied = False
            else:
                st.sidebar.error("Erreur lors du chargement de l'image")
                return None
        
        if st.session_state.image_loaded:
            # Contrôles dans la sidebar
            st.sidebar.header("Parametres de Traitement")
            
            # Mode de traitement : rapide ou contrôlé
            treatment_mode = st.sidebar.radio(
                "Mode de traitement",
                ["Contrôlé (curseurs)", "Rapide (boutons)"],
                help="Choisissez entre contrôle fin par curseurs ou traitements rapides par boutons"
            )
            
            st.sidebar.markdown("---")
            
            if treatment_mode == "Contrôlé (curseurs)":
                # Ajustements photométriques
                st.sidebar.subheader("Ajustements Photometriques")
                brightness = st.sidebar.slider("Luminosite", -100, 100, 0, 5)
                contrast = st.sidebar.slider("Contraste", 0.1, 3.0, 1.0, 0.1)
                gamma = st.sidebar.slider("Gamma", 0.1, 3.0, 1.0, 0.1)
                
                # Transformations géométriques
                st.sidebar.subheader("Transformations Geometriques")
                rotation = st.sidebar.slider("Rotation (degres)", -180, 180, 0, 5)
                blur_kernel = st.sidebar.slider("Noyau de flou", 1, 15, 1, 2)
                
                # Filtres
                st.sidebar.subheader("Filtres")
                filter_type = st.sidebar.selectbox(
                    "Type de filtre",
                    ["Aucun", "Gaussien", "Median", "Bilateral", "Nettete"]
                )
                
                # Seuillage
                st.sidebar.subheader("Seuillage")
                threshold_type = st.sidebar.selectbox(
                    "Type de seuillage",
                    ["Aucun", "Global Manuel", "Otsu", "Adaptatif Moyenne", "Adaptatif Gaussien"]
                )
                block_size = st.sidebar.slider("Block Size", 3, 31, 11, 2)
                c_value = st.sidebar.slider("C (Constante)", 0, 10, 2, 1)
                
                if threshold_type == "Global Manuel":
                    threshold_value = st.sidebar.slider("Seuil", 0, 255, 127, 5)
                else:
                    threshold_value = 127
                
                # Égalisation
                st.sidebar.subheader("Egalisation d'Histogramme")
                equalization_type = st.sidebar.selectbox(
                    "Type d'egalisation",
                    ["Aucune", "Globale", "CLAHE"]
                )
                
                # Opérations morphologiques
                st.sidebar.subheader("Operations Morphologiques")
                morph_operation = st.sidebar.selectbox(
                    "Operation",
                    ["Aucune", "Erosion", "Dilatation", "Ouverture", "Fermeture"]
                )
                morph_kernel_size = st.sidebar.slider("Taille noyau morphologique", 3, 15, 3, 2)
                
                # Détection de contours
                st.sidebar.subheader("Detection de Contours")
                edge_detection = st.sidebar.selectbox(
                    "Methode",
                    ["Aucune", "Canny", "Sobel", "Laplacien"]
                )
                
                if edge_detection == "Canny":
                    canny_low = st.sidebar.slider("Seuil bas Canny", 0, 255, 50, 5)
                    canny_high = st.sidebar.slider("Seuil haut Canny", 0, 255, 150, 5)
                else:
                    canny_low = 50
                    canny_high = 150
                
                # Bouton de réinitialisation pour le mode contrôlé
                st.sidebar.markdown("---")
                if st.sidebar.button("Reinitialiser"):
                    self.processor.reset_image()
                    st.session_state.treatment_applied = False
                
                # Retourner les paramètres pour le mode contrôlé
                return {
                    'mode': 'controlled',
                    'brightness': brightness,
                    'contrast': contrast,
                    'gamma': gamma,
                    'rotation': rotation,
                    'blur_kernel': blur_kernel,
                    'filter_type': filter_type,
                    'threshold_type': threshold_type,
                    'threshold_value': threshold_value,
                    'equalization_type': equalization_type,
                    'morph_operation': morph_operation,
                    'morph_kernel_size': morph_kernel_size,
                    'edge_detection': edge_detection,
                    'canny_low': canny_low,
                    'canny_high': canny_high
                }
            
            else:  # Mode rapide avec boutons
                # Boutons de traitement rapide
                st.sidebar.subheader("Traitements Rapides")
                
                col1, col2 = st.sidebar.columns(2)
                
                with col1:
                    if st.button("Egalisation Globale"):
                        self.processor.equalize_histogram_global()
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Filtre Gaussien"):
                        self.processor.apply_gaussian_blur(5)
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Contours Canny"):
                        self.processor.detect_edges_canny(50, 150)
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Rehaussement"):
                        self.processor.apply_sharpening()
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                
                with col2:
                    if st.button("Egalisation CLAHE"):
                        self.processor.equalize_histogram_clahe()
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Filtre Median"):
                        self.processor.apply_median_filter(5)
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Seuillage Otsu"):
                        self.processor.apply_threshold_otsu()
                        st.session_state.treatment_applied = True
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = self.processor.processed_image.copy()
                    
                    if st.button("Reinitialiser"):
                        self.processor.reset_image()
                        st.session_state.treatment_applied = False
                        st.session_state.mode = 'quick'
                        st.session_state.saved_processed_image = None
                
                # Retourner les paramètres pour le mode rapide
                return {
                    'mode': 'quick'
                }
        
        return None
    
    def apply_slider_treatments(self, params):
        """
        Appliquer les traitements basés sur les curseurs
        Seulement si on est en mode contrôlé
        
        Args:
            params: Dictionnaire des paramètres
        """
        # N'appliquer les curseurs que si on est en mode contrôlé
        if params.get('mode') != 'controlled':
            return
        
        # Vérifier que l'image originale existe
        if self.processor.original_image is None:
            return
        
        # Commencer avec l'image originale
        result = self.processor.original_image.copy()
        
        # 1. Luminosité et contraste
        if params['brightness'] != 0 or params['contrast'] != 1.0:
            result = cv2.convertScaleAbs(result, alpha=params['contrast'], beta=params['brightness'])
        
        # 2. Gamma
        if params['gamma'] != 1.0:
            inv_gamma = 1.0 / params['gamma']
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            result = cv2.LUT(result, table)
        
        # 3. Rotation
        if params['rotation'] != 0:
            h, w = result.shape[:2]
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, params['rotation'], 1.0)
            result = cv2.warpAffine(result, matrix, (w, h))
        
        # 4. Filtres
        if params['filter_type'] == "Gaussien":
            result = cv2.GaussianBlur(result, (params['blur_kernel'], params['blur_kernel']), 0)
        elif params['filter_type'] == "Median":
            kernel_size = params['blur_kernel']
            if kernel_size % 2 == 0:
                kernel_size += 1
            result = cv2.medianBlur(result, kernel_size)
        elif params['filter_type'] == "Bilateral":
            result = cv2.bilateralFilter(result, 9, 75, 75)
        elif params['filter_type'] == "Nettete":
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            result = cv2.filter2D(result, -1, kernel)
        
        # 5. Seuillage
        if params['threshold_type'] != "Aucun":
            if len(result.shape) == 3:
                gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            else:
                gray = result
            
            if params['threshold_type'] == "Global Manuel":
                _, binary = cv2.threshold(gray, params['threshold_value'], 255, cv2.THRESH_BINARY)
            elif params['threshold_type'] == "Otsu":
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif params['threshold_type'] == "Adaptatif Moyenne":
                binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            elif params['threshold_type'] == "Adaptatif Gaussien":
                binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            
            result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        # 6. Égalisation
        if params['equalization_type'] == "Globale":
            if len(result.shape) == 3:
                yuv = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)
                yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
                result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            else:
                result = cv2.equalizeHist(result)
        elif params['equalization_type'] == "CLAHE":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            if len(result.shape) == 3:
                yuv = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)
                yuv[:,:,0] = clahe.apply(yuv[:,:,0])
                result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            else:
                result = clahe.apply(result)
        
        # 7. Opérations morphologiques
        if params['morph_operation'] != "Aucune":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (params['morph_kernel_size'], params['morph_kernel_size']))
            
            if params['morph_operation'] == "Erosion":
                result = cv2.erode(result, kernel, iterations=1)
            elif params['morph_operation'] == "Dilatation":
                result = cv2.dilate(result, kernel, iterations=1)
            elif params['morph_operation'] == "Ouverture":
                result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
            elif params['morph_operation'] == "Fermeture":
                result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        
        # 8. Détection de contours
        if params['edge_detection'] != "Aucune":
            if len(result.shape) == 3:
                gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            else:
                gray = result
            
            if params['edge_detection'] == "Canny":
                edges = cv2.Canny(gray, params['canny_low'], params['canny_high'])
                result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            elif params['edge_detection'] == "Sobel":
                sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
                magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
                result = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2BGR)
            elif params['edge_detection'] == "Laplacien":
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                laplacian = np.absolute(laplacian)
                laplacian = np.clip(laplacian, 0, 255).astype(np.uint8)
                result = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
        
        self.processor.processed_image = result
    
    def display_images(self):
        """Afficher les images originale et traitée"""
        if not st.session_state.image_loaded:
            st.info("Veuillez charger une image pour commencer le traitement.")
            return
        
        # Vérifier que l'image originale existe
        if self.processor.original_image is None:
            st.error("L'image originale n'est plus disponible. Veuillez recharger une image.")
            st.session_state.image_loaded = False
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Image Originale")
            original_pil = self.visualizer.convert_to_pil(self.processor.original_image)
            st.image(original_pil, caption="Image chargee", use_container_width=True)
        
        with col2:
            st.subheader("Image Traitee")
            # Utiliser l'image sauvegardée si elle existe, sinon l'image traitée actuelle
            if st.session_state.saved_processed_image is not None:
                processed_pil = self.visualizer.convert_to_pil(st.session_state.saved_processed_image)
            else:
                processed_pil = self.visualizer.convert_to_pil(self.processor.processed_image)
            st.image(processed_pil, caption="Image traitee avec les parametres actuels", use_container_width=True)
    
    def display_statistics(self):
        """Afficher les statistiques comparatives"""
        if not st.session_state.image_loaded:
            return
        
        # Vérifier que l'image originale existe
        if self.processor.original_image is None:
            st.error("L'image originale n'est plus disponible. Veuillez recharger une image.")
            st.session_state.image_loaded = False
            return
        
        st.markdown("---")
        st.subheader("Analyse et Informations")
        
        # Utiliser l'image sauvegardée si elle existe, sinon l'image traitée actuelle
        if st.session_state.saved_processed_image is not None:
            processed_image = st.session_state.saved_processed_image
        else:
            processed_image = self.processor.processed_image
        
        # Obtenir les statistiques
        original_stats = self.processor.get_image_stats(self.processor.original_image)
        processed_stats = self.processor.get_image_stats(processed_image)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Dimensions", f"{original_stats['shape'][1]}×{original_stats['shape'][0]}")
            st.metric("Canaux", original_stats['channels'])
        
        with col2:
            st.metric("Luminance moyenne", f"{original_stats['mean']:.1f}")
            st.metric("Ecart-type", f"{original_stats['std']:.1f}")
        
        with col3:
            st.metric("Nouvelle luminance", f"{processed_stats['mean']:.1f}")
            st.metric("Nouvel ecart-type", f"{processed_stats['std']:.1f}")
        
        # Graphique comparatif
        fig = self.visualizer.plot_statistics_comparison(original_stats, processed_stats)
        st.pyplot(fig)
    
    def display_histograms(self):
        """Afficher les histogrammes comparatifs"""
        if not st.session_state.image_loaded:
            return
        
        # Vérifier que l'image originale existe
        if self.processor.original_image is None:
            st.error("L'image originale n'est plus disponible. Veuillez recharger une image.")
            st.session_state.image_loaded = False
            return
        
        st.subheader("Histogrammes")
        
        # Utiliser l'image sauvegardée si elle existe, sinon l'image traitée actuelle
        if st.session_state.saved_processed_image is not None:
            processed_image = st.session_state.saved_processed_image
        else:
            processed_image = self.processor.processed_image
        
        fig = self.visualizer.plot_comparison_histograms(
            self.processor.original_image, 
            processed_image
        )
        st.pyplot(fig)
    
    def display_download_section(self):
        """Afficher la section de téléchargement"""
        if not st.session_state.image_loaded:
            return
        
        # Vérifier que l'image originale existe
        if self.processor.original_image is None:
            st.error("L'image originale n'est plus disponible. Veuillez recharger une image.")
            st.session_state.image_loaded = False
            return
        
        st.markdown("---")
        st.subheader("Telechargement")
        
        # Utiliser l'image sauvegardée si elle existe, sinon l'image traitée actuelle
        if st.session_state.saved_processed_image is not None:
            download_image = st.session_state.saved_processed_image
        else:
            download_image = self.processor.processed_image
        
        # Convertir en bytes pour le téléchargement
        _, buffer = cv2.imencode('.jpg', download_image)
        
        st.download_button(
            label="Telecharger l'image traitee",
            data=buffer.tobytes(),
            file_name="image_traitee.jpg",
            mime="image/jpeg"
        )
        
        # Option: Télécharger la fiche récapitulative
        if st.button("Generer fiche recapitulative"):
            original_stats = self.processor.get_image_stats(self.processor.original_image)
            processed_stats = self.processor.get_image_stats(download_image)
            treatment_history = self.processor.get_treatment_history()
            
            fig = self.visualizer.create_treatment_summary(
                self.processor.original_image,
                download_image,
                treatment_history,
                original_stats,
                processed_stats
            )
            
            st.pyplot(fig)
    
    def display_instructions(self):
        """Afficher les instructions d'utilisation"""
        st.markdown("---")
        st.subheader("Instructions d'utilisation")
        
        st.markdown("""
        ### Comment utiliser cette application:
        
        1. **Charger une image** : Utilisez le bouton dans la barre latérale
        2. **Ajuster les paramètres** : Utilisez les curseurs pour modifier l'image en temps réel
        3. **Appliquer des filtres** : Choisissez parmi différents types de filtres
        4. **Utiliser les traitements rapides** : Cliquez sur les boutons pour des effets prédéfinis
        5. **Analyser les résultats** : Consultez les histogrammes et les statistiques
        6. **Telecharger** : Sauvegardez votre image traitée
        
        ### Fonctionnalités disponibles:
        
        - **Ajustements photométriques** : Luminosité, contraste, gamma
        - **Transformations géométriques** : Rotation, redimensionnement
        - **Filtrage spatial** : Gaussien, médian, bilatéral, netteté
        - **Détection de contours** : Canny, Sobel, Laplacien
        - **Seuillage** : Global manuel, Otsu, adaptatif
        - **Opérations morphologiques** : Érosion, dilatation, ouverture, fermeture
        - **Égalisation d'histogramme** : Globale, CLAHE
        - **Analyse d'histogramme** : Visualisation et statistiques
        
        ### Conseils:
        
        - Utilisez l'égalisation **CLAHE** pour un contraste local optimal
        - Le filtre **médian** est excellent pour le bruit "poivre et sel"
        - La correction **gamma** offre un contrôle plus fin que la luminosité
        - Les **contours Canny** sont parfaits pour la détection d'objets
        - Le seuillage **adaptatif** est idéal pour les images avec éclairage irrégulier
        - Les opérations **morphologiques** affinent les contours et éliminent le bruit
        """)
    
    def display_footer(self):
        """Afficher le pied de page"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            Plateforme Intelligente d'Analyse d'Images<br>
            by <a href="https://oumou100.github.io/" target="_blank">oumouDev</a>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Exécuter l'interface complète"""
        # Configuration de la page
        self.setup_page()
        
        # Créer la sidebar
        params = self.create_sidebar()
        
        if st.session_state.image_loaded and params is not None:
            # Appliquer les traitements selon le mode
            if params.get('mode') == 'controlled':
                # Mode contrôlé : appliquer les curseurs
                self.apply_slider_treatments(params)
            # Mode rapide : les traitements sont déjà appliqués par les boutons
            
            # Afficher les sections
            self.display_images()
            self.display_statistics()
            self.display_histograms()
            self.display_download_section()
        else:
            # Afficher les instructions
            self.display_instructions()
        
        # Pied de page
        self.display_footer()

def main():
    """Fonction principale"""
    interface = StreamlitInterface()
    interface.run()

if __name__ == "__main__":
    main()
