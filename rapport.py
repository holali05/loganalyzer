#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
# On importe le chemin défini dans la config globale
from config import RAPPORTS_DIR

def generer_rapport(data):
    """
    Transforme le dictionnaire de données en un fichier JSON.
    Sauvegarde le fichier dans le dossier RAPPORTS_DIR avec un nom horodaté.
    
    Args:
        data (dict): Le dictionnaire structuré provenant de analyser.py
        
    Returns:
        str: Le chemin absolu du fichier généré.
    """
    
    # 1. Construction du nom de fichier : rapport_YYYY-MM-DD.json
    # On utilise datetime pour garantir le format demandé
    date_du_jour = datetime.now().strftime("%Y-%m-%d")
    nom_fichier = f"rapport_{date_du_jour}.json"
    
    # 2. Construction du chemin absolu
    # Le sujet insiste sur l'usage de chemins absolus.
    # Bien que RAPPORTS_DIR soit déjà absolu via config.py, 
    # on s'assure ici de la robustesse du chemin final.
    chemin_complet = os.path.abspath(os.path.join(RAPPORTS_DIR, nom_fichier))

    # 3. Vérification de la structure (optionnel mais recommandé par tes règles)
    if not isinstance(data, dict) or "metadata" not in data:
        raise ValueError("Le format de données fourni est invalide.")

    try:
        # 4. Écriture du fichier JSON
        # indent=4 pour un fichier "propre" et lisible
        # ensure_ascii=False pour gérer correctement les accents français
        with open(chemin_complet, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return chemin_complet

    except (IOError, OSError) as e:
        # Règle critique : On lève une exception, on ne fait pas de print
        raise RuntimeError(f"Erreur fatale lors de l'écriture du rapport JSON : {e}")