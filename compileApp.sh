#!/bin/bash

.venv/bin/pyinstaller --onefile --add-data "memRanobe_MangaLib.json:." --add-data "memRawWithArgs.json:." --add-data "Icons:Icons" --name SiteNotify main.py

echo "All Done!"
