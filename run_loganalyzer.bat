@echo off
cd /d C:\loganalyzer
python main.py --source logs_test --dest backups --retention 30 >> C:\loganalyzer\cron_windows.log 2>&1
