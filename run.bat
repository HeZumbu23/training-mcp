@echo off
REM Installiert Abhaengigkeiten (falls noetig) und startet den dummy-mcp-server.
set SCRIPT_DIR=%~dp0
pip install -q -r "%SCRIPT_DIR%requirements.txt"
python "%SCRIPT_DIR%server.py" %*
