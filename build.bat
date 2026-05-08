@echo off

echo Cleaning old builds...
rmdir /s /q build
rmdir /s /q dist

echo Building exe...

python -m PyInstaller --onefile --windowed ^
--hidden-import=requests ^
--hidden-import=bs4 ^
--hidden-import=torch ^
--hidden-import=transformers ^
--hidden-import=tokenizers ^
news.py

echo Done!
pause