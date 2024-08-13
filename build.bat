@echo off
pyinstaller --name=EchoG --onefile --windowed --icon=res/icon.png --add-data="res;res" main.py
pause