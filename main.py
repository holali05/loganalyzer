#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse

from config import (
    ensure_directories,
    validate_source_dir,
    get_abs_path,
    BACKUPS_DIR
)

from analyser import analyser_logs
from rapport import generer_rapport
from archiver import archiver_logs


def parse_arguments():
    """
    Parse les arguments CLI.
    """
    parser = argparse.ArgumentParser(
        description="LogAnalyzer Pro - Analyse et archivage de logs"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Chemin vers le dossier contenant les fichiers logs"
    )

    parser.add_argument(
        "--niveau",
        default="ALL",
        choices=["ERROR", "WARN", "INFO", "ALL"],
        help="Niveau de filtrage (défaut: ALL)"
    )

    parser.add_argument(
        "--dest",
        default=None,
        help="Dossier de destination pour les archives (optionnel)"
    )

    parser.add_argument(
        "--retention",
        type=int,
        default=30,
        help="Durée de rétention des rapports (en jours)"
    )

    return parser.parse_args()


def main():
    """
    Fonction principale orchestrant le pipeline.
    """
    try:
        # 🔹 1. Initialisation des dossiers
        ensure_directories()

        # 🔹 2. Récupération des arguments
        args = parse_arguments()

        # 🔹 3. Validation des entrées
        source_path = validate_source_dir(args.source)

        if args.retention < 0:
            raise ValueError("La rétention doit être un nombre positif")

        # 🔹 4. Gestion du chemin de destination (ABSOLU obligatoire)
        dest_path = get_abs_path(args.dest) if args.dest else BACKUPS_DIR

        print(f"[INFO] Source : {source_path}")
        print(f"[INFO] Niveau : {args.niveau}")
        print(f"[INFO] Destination archive : {dest_path}")
        print(f"[INFO] Rétention : {args.retention} jours")

        # 🔹 5. Analyse des logs
        print("[INFO] Analyse en cours...")
        data = analyser_logs(source_path, args.niveau)

        # 🔹 Sécurisation du format data
        if not isinstance(data, dict):
            raise TypeError("analyser_logs doit retourner un dictionnaire")

        if "metadata" not in data:
            data["metadata"] = {}

        data["metadata"]["source"] = source_path

        # 🔹 6. Génération du rapport
        print("[INFO] Génération du rapport...")
        rapport_path = generer_rapport(data)

        print(f"[SUCCESS] Rapport généré : {rapport_path}")

        # 🔹 7. Archivage + nettoyage
        print("[INFO] Archivage en cours...")
        archiver_logs(
            fichiers=data.get("fichiers_traites", []),
            dest=dest_path,
            retention=args.retention
        )

        print("[SUCCESS] Archivage terminé")
        print("[DONE] Pipeline exécuté avec succès")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()