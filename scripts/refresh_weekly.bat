@echo off
cd /d E:\DataAnalyst\trend-analysis
python scripts\refresh_weekly.py >> data\_refresh_log.txt 2>&1
