@echo off

nuitka --onefile --plugin-enable=pylint-warnings --include-plugin-directory=pygame_gui/data --include-data-dir=assets=package/assets -o quan3t.exe --output-dir=package main.py
md package\app\assets 2>nul
move package\quan3t.exe package\app\quan3t.exe
copy assets\*.* package\app\assets
powershell Compress-Archive -Path package\app -DestinationPath package\quan3t.zip