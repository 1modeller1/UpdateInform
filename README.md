# UpdateInform

Это приложение для отслеживания обновлений на выбранных вами сайтах. Раз в определенные интервалы времени оно будет сканировать и проверять, появилось ли что-либо новое на сайтах, обновления на которых вас интересуют.
Более подробно о работе с приложением в guide.md.

Для того, чтобы забилдить приложение в linux, используйте:
```
$ chmod +x buildApp.sh
$ ./buildApp.sh
```
В Windows пропешите в терминале:

```
pyinstaller --onefile --windowed --add-data "screens;screens" --add-data "Icons;Icons" --add-data "guide.md;." --name SiteNotify --exclude PySide6 --exclude PyQt5 main.py
```
