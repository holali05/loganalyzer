LogAnalyzer Pro
C'est quoi ?
LogAnalyzer Pro est un script Python qui automatise l'analyse de fichiers logs. Tu lui donnes un dossier, il lit tous les .log dedans, compte les erreurs, génère un rapport JSON et archive les fichiers traités. Idéal pour garder un œil sur les systèmes sans tout faire à la main.

Ce qu'il faut pour l'utiliser

Python 3.6 minimum
Windows, Linux ou macOS — ça marche sur les trois
Aucune librairie externe à installer, tout est dans la bibliothèque standard Python


Installation
bashgit clone https://github.com/holali05/loganalyzer.git
cd loganalyzer
python --version  # vérifier que tu as bien Python 3.6+

Comment lancer le script
bashpython main.py --source CHEMIN_VERS_TES_LOGS [OPTIONS]

Les options disponiblesLe script accepte quatre arguments en ligne de commande. Un seul est obligatoire, les trois autres ont des valeurs par défaut si tu ne les précises pas.--source (obligatoire)
Le chemin vers le dossier qui contient tes fichiers .log. Sans cet argument, le script ne peut pas démarrer.--niveau (optionnel, défaut : ALL)
Permet de filtrer les logs selon leur niveau de criticité. Si tu ne mets rien, tous les niveaux sont analysés. Les valeurs possibles sont :

ALL — analyse tout sans exception
ERROR — seulement les lignes marquées comme erreurs
WARN — les erreurs et les avertissements
INFO — tous les niveaux standards (ERROR, WARN, INFO)
--dest (optionnel, défaut : ./backups)
Le dossier où seront stockées les archives générées après l'analyse. Par défaut, un dossier backups/ est créé automatiquement dans le répertoire courant.--retention (optionnel, défaut : 30)
Indique combien de jours les rapports doivent être conservés avant d'être supprimés automatiquement. Utile pour éviter que les anciens rapports ne s'accumulent indéfiniment.


Exemples concrets
bash# Analyse basique
python main.py --source /var/log/application

# Seulement les erreurs
python main.py --source /var/log/application --niveau ERROR

# Avec un dossier d'archive personnalisé et rétention de 90 jours
python main.py --source /var/log/application --dest /mnt/archives/logs --retention 90

# Sur Windows, avec filtrage WARN
python main.py --source C:\logs\app --niveau WARN --dest D:\backups --retention 60
```

---

## Format attendu des fichiers logs

Chaque ligne doit suivre ce format :
```
YYYY-MM-DD HH:MM:SS NIVEAU Message
```

Exemple :
```
2024-01-15 10:30:15 ERROR Database connection failed
2024-01-15 10:31:20 WARN High memory usage detected
2024-01-15 10:32:05 INFO User login successful

Structure du projet
Le projet est découpé en six fichiers Python, chacun avec une responsabilité bien précise.
main.py — C'est le point d'entrée du programme. Il récupère les arguments passés en ligne de commande, vérifie qu'ils sont valides, puis appelle les autres modules dans le bon ordre pour exécuter le pipeline complet.
analyser.py — C'est le cœur de l'analyse. Il parcourt le dossier source, lit chaque fichier .log ligne par ligne, et comptabilise les entrées par niveau (ERROR, WARN, INFO). Il identifie aussi les 5 messages d'erreur qui reviennent le plus souvent.
rapport.py — Une fois l'analyse terminée, ce module prend les résultats et génère un fichier JSON structuré. Ce rapport inclut les statistiques, mais aussi des métadonnées comme la date d'exécution, le système d'exploitation et le chemin source.
archiver.py — Il compresse les fichiers logs traités dans une archive .tar.gz et la dépose dans le dossier de destination. Il applique aussi la politique de rétention en supprimant automatiquement les rapports plus anciens que la durée configurée.
config.py — Centralise toute la configuration du projet : les chemins des dossiers, les constantes (niveaux de logs, etc.) et les fonctions qui vérifient que les chemins sont valides. Il crée aussi les dossiers nécessaires s'ils n'existent pas encore.
utils.py — Regroupe des fonctions utilitaires générales réutilisées par les autres modules : manipulation de fichiers, formatage de données, conversions, etc.

Automatisation avec Cron (Linux/macOS)
Pour lancer l'analyse automatiquement chaque dimanche à minuit :
bashcrontab -e
Ajoute cette ligne :
bash0 0 * * 0 /usr/bin/python3 /chemin/vers/loganalyzer/main.py --source /var/log/app --dest /mnt/backups/logs
Autres fréquences possibles :

Tous les jours à minuit : 0 0 * * *
Dimanche et mercredi : 0 0 * * 0,3
Le 1er de chaque mois : 0 0 1 * *


Organisation de l'équipe
Le projet a été développé en équipe avec une répartition claire des rôles, chaque membre étant responsable d'un module précis.
Étudiant A — Lead / Architecte
Responsable de main.py. Il gère le point d'entrée du programme, l'orchestration générale et s'assure de la cohérence des chemins avec le module os.path. C'est lui qui garantit que les différents modules communiquent correctement entre eux.
Étudiant B — Analyste
Responsable de analyser.py. Il implémente toute la logique de parsing des fichiers logs : lecture ligne par ligne, détection des niveaux de criticité et extraction des erreurs les plus fréquentes.
Étudiant C — Data Manager
Responsable de rapport.py. Il s'occupe de la mise en forme des résultats d'analyse en JSON, en veillant à ce que la structure du rapport soit claire, complète et exploitable.
Étudiant D — SysAdmin
Responsable de archiver.py. Il gère la compression des logs avec tarfile, le nettoyage des anciens fichiers selon la politique de rétention et la surveillance de l'espace disque utilisé.
Étudiant E — QA / Documentation
Responsable de la qualité et de la documentation. Il prépare les fichiers de tests dans logs_test/, rédige le README et configure la ligne Cron pour la planification automatique hebdomadaire.