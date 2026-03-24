#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import glob

def analyser_logs(source_path, niveau="ALL"):
    """
    Scanne le dossier source, filtre les logs par niveau et calcule les stats.
    Retourne un dictionnaire structuré pour les modules de rapport et d'archivage.
    """
    # 1. Initialisation de la structure de données
    data = {
        "metadata": {
            "date": "", # Sera rempli par le module rapport.py
            "utilisateur": os.environ.get('USER') or os.environ.get('USERNAME', 'Inconnu'),
            "os": platform.system(),
            "source": os.path.abspath(source_path)
        },
        "statistiques": {
            "total_lignes": 0,
            "par_niveau": {"ERROR": 0, "WARN": 0, "INFO": 0},
            "top5_erreurs": []
        },
        "fichiers_traites": []
    }

    compteur_erreurs = {}

    # 2. Récupération des fichiers .log
    source_abs = os.path.abspath(source_path)
    search_pattern = os.path.join(source_abs, "*.log")
    fichiers = glob.glob(search_pattern)

    if not fichiers:
        raise FileNotFoundError(f"Aucun fichier .log trouvé dans {source_path}")

    data["fichiers_traites"] = fichiers
    
    # 3. Analyse ligne par ligne
    for chemin_fichier in fichiers:
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if not ligne:
                        continue  

                    # Format attendu : YYYY-MM-DD HH:MM:SS NIVEAU Message
                    parties = ligne.split(' ', 3)
                    if len(parties) < 4:
                        continue 

                    log_niveau = parties[2].upper() 
                    log_message = parties[3]

                    # 4. Filtrage et Statistiques
                    if niveau == "ALL" or log_niveau == niveau:
                        data["statistiques"]["total_lignes"] += 1
                        
                        if log_niveau in data["statistiques"]["par_niveau"]:
                            data["statistiques"]["par_niveau"][log_niveau] += 1
                        
                        # On ne garde que les messages ERROR pour le Top 5
                        if log_niveau == "ERROR":
                            compteur_erreurs[log_message] = compteur_erreurs.get(log_message, 0) + 1

        except Exception as e:
            raise RuntimeError(f"Erreur de lecture sur {os.path.basename(chemin_fichier)} : {e}")

    # 5. Calcul du Top 5
    top5 = sorted(compteur_erreurs.items(), key=lambda x: x[1], reverse=True)[:5]
    data["statistiques"]["top5_erreurs"] = [msg for msg, count in top5]

    return data