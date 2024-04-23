@echo off
setlocal

set "user_dir=%USERPROFILE%"

cd %user_dir%\sistema\api-main\API
call ..\Scripts\activate

python run.py

endlocal
