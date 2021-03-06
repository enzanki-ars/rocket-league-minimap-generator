CALL .\.venv\Scripts\activate
pip install -r .\requirements.txt
set PYTHONOPTIMIZE=1 && pyinstaller .\rocketleaguereplayanalysis\main.py --onefile

MOVE /Y .\dist\main.exe .\dist\rocketleaguereplayanalysis.exe
COPY /Y .\README.md .\dist\README.txt
DEL /S /Q .\dist\assets
COPY /Y .\assets .\dist\assets

powershell Compress-Archive -Force -Path .\dist\rocketleaguereplayanalysis.exe, .\dist\README.txt, .\dist\assets -DestinationPath .\dist\rocketleaguereplayanalysis.zip

pause
