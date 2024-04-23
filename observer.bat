@echo off

set "user_dir=%USERPROFILE%"

call %user_dir%\sistema\api-main\Scripts\activate.bat

cd %user_dir%\sistema\api-main\API

:loop
tasklist /fi "imagename eq python.exe" | find "run.py" > nul
if errorlevel 1 (
    python run.py
)
timeout /t 5 /nobreak > nul
goto loop
