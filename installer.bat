@echo off
cd /d "%~dp0"
python -m venv .venv
if errorlevel 1 goto error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Installation terminee. Lance maintenant lancer.bat.
pause
exit /b 0
:error
echo Installation impossible. Consulte README.md et verifie Python et Internet.
pause
exit /b 1
