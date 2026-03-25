# LogAnalyzer Pro

Outil CLI pour analyser, générer des rapports JSON, archiver et nettoyer automatiquement les logs applicatifs.

---

## 1. Description du projet

LogAnalyzer Pro est un outil en ligne de commande permettant de :  

- Scanner un dossier contenant des fichiers `.log`.  
- Filtrer les logs selon leur niveau de criticité (`INFO`, `WARN`, `ERROR` ou `ALL`).  
- Générer un rapport structuré au format JSON avec des statistiques.  
- Archiver les fichiers traités dans un fichier `.tar.gz`.  
- Nettoyer automatiquement les anciens rapports selon une politique de rétention.  
- S’exécuter automatiquement via Cron sans intervention humaine.

---

## 2. Prérequis et Installation

- Python 3.10 ou supérieur  
- Aucune bibliothèque externe requise  
- Cloner ou télécharger le projet, puis naviguer dans le dossier `loganalyzer`.

---

## 3. Utilisation

### Analyse des logs
python3 main.py --source C:\loganalyzer\logs_test --niveau ERROR

### Archivage et nettoyage
python3 archiver.py --source C:\loganalyzer\logs_test --dest C:\loganalyzer\backups --retention 30

> `--retention 30` supprime les anciens rapports de plus de 30 jours.

---

## 4. Modules

- **analyser.py** : analyse et filtre les logs, calcule les statistiques
- **rapport.py** : génère le rapport JSON horodaté
- **archiver.py** : archive les logs et supprime les anciens rapports
- **main.py** : orchestre tous les modules

## 5. Ligne Cron

Exemple pour exécuter le script automatiquement tous les dimanches à 03h00 :

0 3 * * 0 python3 C:\loganalyzer\main.py --source C:\loganalyzer\logs_test --niveau ALL

## 6. Répartition des tâches

- **Ashley SEGNON** : Préparation des fichiers de test (logs_test/), rédaction du README, ligne Cron
- **Autres membres** : Implémentation des modules analyser.py, rapport.py, archiver.py, main.py