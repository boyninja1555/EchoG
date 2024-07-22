@echo off
pyinstaller --name=EchoB --onefile --windowed --icon=res/icon.png --add-data="res;res" main.py
pause