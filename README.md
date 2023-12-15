# OpenclassroomsProject4
Développez un programme logiciel en Python

Project 4 of OpenClassrooms Path: Developer Python - Chess Tournament -- create a console based Chess Tournament 
program 


## Prérequis :
    - python 3.10.7
    - pip
    - pyinputplus
    - pandas 
    - tinyDB
    - flake8

## Installation
          open terminal
        - `git clone https://github.com/A1zenAttaqi/ChessTournamentManagerApp.git`
        - Créez l’environnement virtuel du projet : py -m venv .venv
        - Activez l’environnement virtuel : .venv\Scripts\activate
        - Installer les modules : pip install -r requirements.txt
        - `python3 main.py`

## Contenu
    - Un répertoire data (données des tables players, tournaments de tinydb)
    - Un répertoire flake8_rapport contenant le fichier HTML généré par flake8
    - les répertoires models, views et controllers
    - Le fichier main.py permettant d'exécuter l'application
    - Le fichier requirements
    - Le fichier flake8
    - Le fichier README

## Utilisation
### Remarques générales
    Le logiciel comporte un menu principal, qui propose 3 sous-menus :
    - MENU JOUEURS : section dédiée à l'ajout des joueurs de la base de données du programme, voir les détails d'un joueur donné et la liste de tout les joueurs.
    - MENU TOURNOIS : section dédiée à la gestion d'un tournoi d'échecs, elle permet de gérer 1 tournoi à la fois et fonctionne par états.
    - MENU RAPPORTS : section dédiée à l'affichage des joueurs et tournois.
    Elle permet d'afficher la liste des tournois et celle des joueurs, tours et matchs du tournoi sélectionné.

### Déroulement d'un tournoi

    1- Exécutez le programme depuis la console :
        Pour afficher le MAIN MENU , saisir : py main.py

    2- Choisir un sous-menu :
        2.1 MENU JOUEURS :
            - Créer un nouveau joueur
            - Voir les détails d'un joueur
            - Voir la liste de tout les joueurs
        2.2 MENU TOURNOIS :
            - Créer un tournoi (8 joueurs et 4 tours par défaut)
            - Lister tout les tournois
            - Selectioner un tournoi ( c'est la meme option qui déclenche le déroulement d'un tournoi )
            - Affecter des joueurs à un tournoi deja crée 
        2.3 MENU RAPPORTS :
            - Afficher la liste des joueurs :
                * Ordre alphabétique
            - Afficher la liste des tournois :
                - Afficher une liste de tout les tournois
                - Afficher le détail d'un tournoi de la liste :
                    * Liste de ses joueurs
                    * Liste de ses tours
                    * Liste de ses matchs

    3- Générer 1 nouveau rapport flake8 (exemple) :
        Pour générer le rapport, saisir : flake8 --max-line-length=119 --format=html --htmldir=flake8_report --exclude=venv

