#!/bin/bash

.venv/bin/pyinstaller --onefile --add-data "screens:screens" --add-data "Icons:Icons" --add-data "guide.md:." --name SiteNotify main.py

echo "All Done!"
