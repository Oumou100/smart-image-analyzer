# Architecture Logicielle - Plateforme Intelligente d'Analyse d'Images

##  Architecture Modulaire Conforme au Cahier des Charges

Cette architecture représente la version finale et propre de l'application, organisée selon les recommandations du cahier des charges pour une séparation claire des responsabilités.

##  Structure des Fichiers

```
/
├── app.py                          # Fichier principal de lancement
├── requirements.txt                 # Dépendances du projet
├── ReadME.md                  # Documentation de l'architecture
└── modules/                        # Package des modules
    ├── __init__.py                  # Initialisation du package
    ├── interface.py                 # Module interface utilisateur
    ├── image_processor.py           # Module traitement d'images
    └── visualization.py            # Module visualisation et graphiques
    |__ressources/                   # Dossier des ressources
```

##  Modules et Leurs Rôles

### 1. **app.py** - Point d'Entrée Principal
**Rôle** : Fichier principal de lancement de l'application

**Fonctionnalités** :
- Import des modules nécessaires
- Configuration initiale
- Lancement de l'interface Streamlit

**Code clé** :
```python
from modules.interface import main

if __name__ == "__main__":
    main()  # Lance l'interface principale
```

### 2. **modules/interface.py** - Interface Utilisateur
**Rôle** : Module interface pour les boutons, sliders et zones d'affichage

**Fonctionnalités** :
- **Chargement d'images** : Support JPG, PNG, BMP, TIFF
- **Mode de traitement** : Radio button pour choisir entre "Contrôlé" et "Rapide"
- **Contrôles interactifs** : Curseurs pour luminosité, contraste, gamma, rotation
- **Boutons rapides** : 8 traitements prédéfinis (égalisation, filtres, contours...)
- **Affichage comparatif** : Images originale et traitée côte à côte
- **Téléchargement** : Export des images traitées et fiches récapitulatives

**Classes principales** :
- `StreamlitInterface` : Classe principale de l'interface

**Méthodes clés** :
- `create_sidebar()` : Crée tous les contrôles de la barre latérale
- `display_images()` : Affiche les images originale et traitée
- `display_statistics()` : Affiche les métriques comparatives
- `display_histograms()` : Affiche les histogrammes comparatifs
- `display_download_section()` : Gère le téléchargement et la fiche récapitulative

### 3. **modules/image_processor.py** - Traitement d'Images
**Rôle** : Module traitement pour les fonctions OpenCV

**Fonctionnalités** :
- **Gestion des images** : Chargement, sauvegarde, réinitialisation
- **Ajustements photométriques** : Luminosité, contraste, gamma
- **Filtres spatiaux** : Gaussien, médian, bilatéral, netteté
- **Seuillage** : Manuel, Otsu, adaptatif (moyenne et gaussien)
- **Égalisation d'histogramme** : Globale et CLAHE
- **Opérations morphologiques** : Érosion, dilatation, ouverture, fermeture
- **Détection de contours** : Canny, Sobel, Laplacien
- **Transformations géométriques** : Rotation, flip, redimensionnement

**Classes principales** :
- `ImageProcessor` : Classe principale de traitement

**Méthodes clés** :
- `load_image()` : Charge une image depuis des bytes
- `adjust_brightness_contrast_gamma()` : Ajustements photométriques
- `apply_gaussian_blur()`, `apply_median_filter()` : Filtres
- `equalize_histogram_global()`, `equalize_histogram_clahe()` : Égalisation
- `detect_edges_canny()`, `detect_edges_sobel()` : Détection de contours
- `get_image_stats()` : Calcule les statistiques de l'image

### 4. **modules/visualization.py** - Visualisation et Graphiques
**Rôle** : Module visualisation pour les histogrammes et comparaisons

**Fonctionnalités** :
- **Conversion d'images** : BGR vers RGB, numpy vers PIL
- **Histogrammes** : RGB et niveaux de gris, comparatifs
- **Graphiques statistiques** : Comparaison avant/après
- **Fiches récapitulatives** : Résumé visuel complet du traitement
- **Affichage côte à côte** : Comparaison visuelle des images

**Classes principales** :
- `Visualizer` : Classe principale de visualisation

**Méthodes clés** :
- `convert_to_pil()` : Convertit les images pour Streamlit
- `create_histogram()` : Crée des histogrammes individuels
- `plot_comparison_histograms()` : Histogrammes comparatifs
- `plot_statistics_comparison()` : Graphiques de statistiques
- `create_treatment_summary()` : Fiche récapitulative complète

##  Flux de Données et Interactions

###  **Comment Lire les Graphiques et Statistiques**

#### 1. **Histogrammes Comparatifs**
- **Courbes bleues** : Image originale
- **Courbes rouges** : Image traitée
- **Axes X** : Valeurs de pixels (0-255)
- **Axes Y** : Fréquence des pixels
- **Interprétation** : 
  - Pic décalé vers la droite = image plus claire
  - Courbe plus étalée = plus de contraste
  - Plusieurs pics = image segmentée

#### 2. **Statistiques Comparatives**
- **Luminance moyenne** : Valeur moyenne des pixels (0=noir, 255=blanc)
- **Écart-type** : Variabilité des valeurs (plus élevé = plus de contraste)
- **Dimensions** : Taille de l'image en pixels
- **Canaux** : Nombre de couches (3=RGB, 1=niveaux de gris)

#### 3. **Fiche Récapitulative**
- **Images côte à côte** : Comparaison visuelle directe
- **Tableau de statistiques** : Chiffres comparatifs
- **Historique des traitements** : Liste des opérations appliquées
- **Graphiques** : Visualisation des différences

###  **Workflow de Traitement**

1. **Chargement** : `app.py` → `interface.py` → `image_processor.py`
2. **Interface** : Utilisateur interagit avec les widgets `interface.py`
3. **Traitement** : `interface.py` appelle les méthodes `image_processor.py`
4. **Visualisation** : `interface.py` utilise `visualization.py` pour afficher
5. **Export** : `interface.py` + `visualization.py` génèrent la fiche récapitulative

##  **Modes de Fonctionnement**

###  **Mode Contrôlé (Curseurs)**
- **Usage** : Contrôle fin et cumulatif
- **Fonctionnement** : Les curseurs modifient l'image en temps réel
- **Avantages** : Précision, combinaison de traitements
- **Cas d'usage** : Ajustements précis, expérimentation

###  **Mode Rapide (Boutons)**
- **Usage** : Traitements uniques et immédiats
- **Fonctionnement** : Chaque bouton applique un traitement spécifique
- **Avantages** : Rapidité, effets prédéfinis
- **Cas d'usage** : Tests rapides, démonstrations
