# **# P2_01_codesource**

### Introduction:
Ce script Python est un exercice réalisé dans le cadre d'une formation chez OpenClassrooms
ilextrait des informations sur les livres présents sur le site Books to Scrape.
Il sauvegarde ces données par catégories de livre sous forme de tableur CSV.
Il télécharge et sauvegarde le fichier image de chaque page produit (un livre par page).

### Présentation de l'arborescence du projet:
*Le développement de ce script c'est fait en 3 parties:*
  1. la branche [Master](https://github.com/RenoFar/P2_01_codesource/tree/master/ "Master") corresponds au premier script permettant de traiter un seul livre choisi
  2. la branche [scrap_categorie](https://github.com/RenoFar/P2_01_codesource/tree/scrap_categorie "scrap_categorie") corresponds au script suivant développé à partir de la première branche, permettant de traiter une seule catégorie de livre choisie
  3. la branche [Scrap_All_Categorie](https://github.com/RenoFar/P2_01_codesource/tree/Scrap_All_Category "Scrap_All_Categorie") corresponds au script final développé à partir de la deuxième branche, permettant de traiter toutes les catégories du site et de télécharger les fichiers images.
  
### Pré-requis:
- langage de programmation Python 3 
- Création d'un environnement virtuel avec le module VenV
- Utilisation d'une CLI (interface en ligne de commande)

### Installation:
1. Cloner le projet depuis cette [page](https://github.com/RenoFar/P2_01_codesource "page")
2. Créer un environnement virtuel dans votre dossier de travail contenant les trois fichiers téléchargés
	- Utilisez la commande dans votre CLI `python -m venv <environment name>`  .
	- Activer l'environnement, exécutez `source env/bin/activate`  (si vous êtes sous Windows, la commande sera `env/Scripts/activate.bat`  )
	- Installer les paquets Python répertoriés dans le fichier `requirements.txt`
		avec la commande `$ pip install -r requirements.txt`
3. Installer les modules à l'aide du fichier requirements.txt avec la commande `pip install -r requirements.txt`
4. Exécuter le script Main.py avec la commande `python Main.py`

### Avertissement:
 - Le script créé 2 dossiers contenant 50 fichiers CSV pour le premier et 50 sous dossiers pour chaque catégorie dans le deuxième dossier, dans lesquels sont enregistrés les images.
 - Il traite les données de 1000 pages et télécharge les images de 1000 autres pages, ce qui fait que sa durée d’exécution est approximativement de 16 minutes (8 minutes par dossier).
