#!/bin/bash

.venv/bin/pyinstaller --onefile --add-data "screens:screens" --add-data "Icons:Icons" --add-data "guide.md:." --name SiteNotify --exclude PySide6 --exclude PyQt5 main.py

echo "All Done!"
