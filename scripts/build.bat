@echo off
pyinstaller --distpath ./build-res/dist --workpath ./build-res/build --name=EchoG --onefile --windowed --icon=../res/icon.png --add-data="../res;res" ../src/main.py