@echo off
set VERSION=1.0.2
pyinstaller --distpath ./build-res/dist --workpath ./build-res/build --name=EchoG_%version% --onefile --windowed --icon=../res/icon.png --add-data="../res;res" ../src/main.py