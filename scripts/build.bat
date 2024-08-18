@echo off
set VERSION=1.0.2
pyinstaller --distpath ./build-res/dist --workpath ./build-res/build --name=EchoG_%VERSION% --onefile --windowed --icon=../res/icon.png ../src/main.py --add-data="../res;res" --collect-all lupa --collect-all bs4