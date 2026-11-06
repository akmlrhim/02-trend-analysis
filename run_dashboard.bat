@echo off
rem Menjalankan dashboard Streamlit sebagai proses mandiri (tidak terikat terminal ini).
cd /d "%~dp0"
start "TrendRiset Dashboard" cmd /c "python -m streamlit run app.py --server.port 8501"
