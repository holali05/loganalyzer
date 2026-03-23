#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 🔹 1. Dossier racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 2. Définition des chemins principaux
LOGS_DIR = os.path.join(BASE_DIR, "logs_test")
RAPPORTS_DIR = os.path.join(BASE_DIR, "rapports")
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")

# 🔹 3. Constantes
LOG_LEVELS = ["ERROR", "WARN", "INFO", "ALL"]


# 🔹 4. Création automatique des dossiers
def ensure_directories():
    """
    Crée automatiquement les dossiers nécessaires s'ils n'existent pas.
    """
    for path in [LOGS_DIR, RAPPORTS_DIR, BACKUPS_DIR]:
        os.makedirs(path, exist_ok=True)


# 🔹 5. Chemin absolu sécurisé
def get_abs_path(path):
    """
    Retourne un chemin absolu à partir d'un chemin donné.
    """
    if path is None:
        return None
    return os.path.abspath(path)


# 🔹 6. Validation du dossier source
def validate_source_dir(source_path):
    """
    Vérifie que le dossier source existe et est un dossier.
    """
    abs_path = get_abs_path(source_path)

    if not os.path.isdir(abs_path):
        raise FileNotFoundError(f"Le dossier source n'existe pas : {abs_path}")

    return abs_path


# 🔹 7. Vérification fichier log
def is_log_file(filename):
    """
    Vérifie si un fichier est un fichier log valide.
    """
    return filename.endswith(".log")