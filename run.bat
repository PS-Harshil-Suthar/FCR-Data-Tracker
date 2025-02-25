@echo off
cd /d "%~dp0venv\Scripts"
call activate
cd /d "%~dp0"
python app.py --reload
