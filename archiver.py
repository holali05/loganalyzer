#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarfile
import shutil
import time
import subprocess
from datetime import datetime
from config import BACKUPS_DIR, RAPPORTS_DIR, ensure_directories

def archiver_logs(fichiers, dest=BACKUPS_DIR, retention=30):
    """
    Archive les fichiers logs et nettoie les anciens rapports.
    Module D : Archivage et Nettoyage.
    """
    # S'assurer que les dossiers de destination existent
    ensure_directories()

    if not fichiers:
        return "Aucun fichier à archiver."

    # 1. VÉRIFICATION ESPACE DISQUE (Contrainte : subprocess)
    _verifier_espace_disque_systeme()

    # 2. PRÉPARATION DE L'ARCHIVE (Contrainte : tarfile mode w:gz)
    nom_archive = f"backup_{datetime.now().strftime('%Y-%m-%d')}.tar.gz"
    # On travaille d'abord sur un chemin absolu pour éviter les erreurs de dossier
    chemin_temp = os.path.abspath(nom_archive)
    
    try:
        # Création de l'archive
        with tarfile.open(chemin_temp, "w:gz") as tar:
            for f in fichiers:
                if os.path.exists(f):
                    # Ajout du fichier (arcname permet de ne pas inclure toute l'arborescence C:\...)
                    tar.add(f, arcname=os.path.basename(f))
                else:
                    # GESTION D'ERREUR : Si un fichier de la liste manque, on stop tout.
                    raise FileNotFoundError(f"Fichier log introuvable : {f}")
        
        # 3. DÉPLACEMENT DE L'ARCHIVE (Contrainte : shutil)
        chemin_final = os.path.join(dest, nom_archive)
        shutil.move(chemin_temp, chemin_final)
        
    except Exception as e:
        # Nettoyage du fichier temporaire en cas d'échec
        if os.path.exists(chemin_temp):
            os.remove(chemin_temp)
        # On relance l'erreur pour que le script principal (main.py) soit au courant
        raise e

    # 4. NETTOYAGE DES RAPPORTS (Contrainte : os.path.getmtime et time.time)
    _nettoyer_anciens_rapports(RAPPORTS_DIR, retention)
    
    return chemin_final

def _verifier_espace_disque_systeme():
    """
    Vérifie l'espace libre via la commande système 'df'.
    Seuil de sécurité : 100 Mo.
    """
    try:
        # Tentative via subprocess (Commande Linux/Unix demandée)
        resultat = subprocess.run(['df', '-Pk', '/'], capture_output=True, text=True, timeout=5)
        
        if resultat.returncode == 0:
            ligne_data = resultat.stdout.splitlines()[1]
            espace_libre_ko = int(ligne_data.split()[3])
            
            # 102400 Ko = 100 Mo
            if espace_libre_ko < 102400:
                raise Exception("Espace disque critique (seuil < 100 Mo).")
        else:
            # Si 'df' échoue (ex: Windows), on utilise le plan B (shutil)
            raise FileNotFoundError

    except (FileNotFoundError, IndexError, Exception):
        # Alternative robuste (shutil) pour Windows ou si subprocess échoue
        usage = shutil.disk_usage("/")
        # 100 * 1024 * 1024 = 100 Mo
        if usage.free < (100 * 1024 * 1024):
            raise Exception("Espace disque insuffisant (Vérification shutil).")

def _nettoyer_anciens_rapports(dossier, jours):
    """
    Supprime les fichiers .json plus vieux que 'jours'.
    """
    maintenant = time.time()
    seuil_secondes = jours * 24 * 3600
    
    # On liste les fichiers dans le dossier rapports/
    if os.path.exists(dossier):
        for nom_fichier in os.listdir(dossier):
            chemin = os.path.join(dossier, nom_fichier)
            
            # On vérifie si c'est un fichier JSON
            if os.path.isfile(chemin) and nom_fichier.endswith(".json"):
                # Calcul de l'âge via getmtime
                age_fichier = maintenant - os.path.getmtime(chemin)
                
                if age_fichier > seuil_secondes:
                    os.remove(chemin)