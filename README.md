# Webscraping

Ce programme python permets de récupérer certaines données des livres vendus sur le site Books to Scrape

## Installation

Installer les librairies du requirements.txt nécessaires à l'execution du programme avec la commande :

```bash
pip install -r requirements.txt
```

## Usage
```python
def extract_cat():
```
Cette fonction liste les différentes pages de catégories de livres

```python
def extract_books(links_cat):
```
Cette fonction liste tous les livres présents dans les catégories

```python
def extract_data(links_books, cat):
```
Cette fonction créer un fichier .CSV pour chaque catégorie dans lequel on trouve le détail suivant pour chaque livre :
- product_page_url
- universal_product_code 
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

L'image de chaque livre est elle aussi téléchargée et insérée dans un dossier Images
