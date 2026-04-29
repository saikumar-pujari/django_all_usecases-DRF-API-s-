@echo off
echo Starting FINAL Django server...

REM Base folder
set BASE=<file_path>
@REM C:\Users\Skipper\Desktop\django

REM Go to correct project (IMPORTANT)
cd /d %BASE%\final

REM Activate virtual environment (you used "env")
call %BASE%\env\Scripts\activate

REM Run server
python manage.py rs

pause