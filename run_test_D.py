from archiver import archiver_logs
from config import LOGS_DIR, BACKUPS_DIR
import os

# 1. On prépare la liste des chemins (ce que l'étudiant B te donnerait)
fichiers_simules = [
    os.path.join(LOGS_DIR, "test1.log"),
    os.path.join(LOGS_DIR, "test2.log"),
]

print("--- TEST DU MODULE ARCHIVER ---")

try:
    # 2. On appelle TA fonction
    # On met une rétention de 0 pour tester si ça supprime tout de suite (optionnel)
    chemin_archive = archiver_logs(fichiers_simules, BACKUPS_DIR, retention=30)
    
    print(f"✅ SUCCÈS : L'archive a été créée ici : {chemin_archive}")
    
    # 3. Vérification visuelle
    if os.path.exists(chemin_archive):
        print(f"🔎 Vérification : Le fichier {os.path.basename(chemin_archive)} existe bien sur le disque.")

except Exception as e:
    print(f"❌ ERREUR : Le module a planté. Message : {e}")