import json
import re
import qdarktheme
from time import mktime, strptime, localtime

from PyQt6.QtCore import QUrl, Qt, QThread, pyqtSignal, QTimer, QWaitCondition
from PyQt6.QtGui import QIcon, QAction, QFont, QColor, QPalette
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QScrollArea, QFormLayout, QInputDialog, QMessageBox, QDialog, QFrame, QSystemTrayIcon, QMenu, QStyle
from PyQt6.QtMultimedia import QSoundEffect

import sys

# import os
# from time import sleep
# from pathlib import Path
from parse import parseUrl, lookParse, parseAll, path, getTime

# =======================================

# CURRENT_DIRECTORY = Path(__file__).resolve().parent
interval = 30
enableNotify = True
enableSound = True
fList = ["memRanobe_MangaLib.json", "memRawWithArgs.json"]

class CheckAllTitlesThread (QThread):
    updateTitlesSignal = pyqtSignal(str)
    responseSignal = pyqtSignal(str)
    notifySignal = pyqtSignal(str)
    def run(self):
        global interval
        while True:
            if interval < 30:
                interval = 30
                print("What are you doing?")
            QThread.sleep(interval*60)
            out = parseAll()
            QThread.sleep(2)
            self.responseSignal.emit(updateResponseLabel(out[0]))
            self.notifySignal.emit(notify(out[1]))
            if out[1] != "":
                self.updateTitlesSignal.emit(changeTimeInTitles())

def checkAllTitles ():
    out = parseAll()
    updateResponseLabel(out[0])
    notify(out[1])
    if out[1] != "":
        changeTimeInTitles()

def changeTimeInTitles ():
    global fList

    now = getTime()
    nTime = strptime(now[7:], "%d.%m.%Y")

    t = 0
    for f in fList:
        f = open(f, "r")
        j = json.load(f)

        for k in j["data"]:
            tim = k["time"]
            lT = box.itemAt(t).layout().itemAt(2).widget()

            lT.setText(tim)

            wTime = strptime(tim, "%H:%M  %d.%m.%Y")
            difference = (mktime(nTime) - mktime(wTime)) / 60 / 60

            if difference < 24:
                lT.setStyleSheet("color : rgb(50,150,50)")
            elif difference < 24*7:
                lT.setStyleSheet("color : rgb(150,150,50)")
            else:
                lT.setStyleSheet("color : grey")

            t += 1
        f.close()

def updateResponseLabel (input):
    labResponse.setText(input)

def clUrlSave ():
    try:
        bUrlInp.setDisabled(True)
        labStatus.setText("Process going ...")
        title = urlInputName.text()
        args = getArgs()

        output = parseUrl(urlInput.text(), title, args)
        labStatus.setText(output[0])
        labResponse.setText(output[1])
        updateTitles()
    except Exception as e:
        labStatus.setText(str(e))
    bUrlInp.setEnabled(True)

def clLookParse ():
    if urlInput.text() != "":
        bUrlLoupe.setDisabled(True)
        args = getArgs()

        try:
            labResponse.setText(lookParse(urlInput.text(), args))
        except Exception as e:
            labStatus.setText(str(e))

        # webWidget.reload()
        bUrlLoupe.setEnabled(True)

def changedUrl ():
    inp = urlInput.text()
    if "ranobelib.me" in inp or "mangalib.me" in inp:
        labStatus.setText("Update will be made automatically")
        inputComplex0.setPlaceholderText("No need")
        inputComplex1.setPlaceholderText("No need")
        inputComplex2.setPlaceholderText("No need")
    else:
        labStatus.setText("")
        inputComplex0.setPlaceholderText("")
        inputComplex1.setPlaceholderText("")
        inputComplex2.setPlaceholderText("")

def clAddParameter ():
    hboxUrlComplex1 = QHBoxLayout()

    inputComplex0 = QLineEdit()
    inputComplex0.setFixedHeight(30)
    inputComplex0.setMaximumWidth(160)

    inputComplex1 = QLineEdit()
    inputComplex1.setFixedHeight(30)
    inputComplex1.setMaximumWidth(120)

    inputComplex2 = QLineEdit()
    inputComplex2.setFixedHeight(30)
    inputComplex2.setMaximumWidth(120)

    bInpComplexMinus = QPushButton()
    bInpComplexMinus.setFixedSize(28, 28)
    bInpComplexMinus.setIcon(QIcon(path("Icons/minus.png")))
    bInpComplexMinus.setFlat(True)
    bInpComplexMinus.clicked.connect(lambda : deleteLayout(hboxUrlComplex1))
    space1 = QLabel()

    hboxUrlComplex1.addWidget(inputComplex0)
    hboxUrlComplex1.addWidget(inputComplex1)
    hboxUrlComplex1.addWidget(inputComplex2)
    hboxUrlComplex1.addWidget(bInpComplexMinus)
    hboxUrlComplex1.addWidget(space1)

    vboxUrlComplex.addLayout(hboxUrlComplex1)

def deleteLayout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)
    layout.setParent(None)

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        for j in reversed(range(layout.itemAt(i).layout().count())):
            layout.itemAt(i).layout().itemAt(j).widget().setParent(None)
        layout.itemAt(i).layout().setParent(None)

def getArgs ():
    args = []
    a = 0
    while True:
        if vboxUrlComplex.itemAt(a) == None:
            break
        i0 = vboxUrlComplex.itemAt(a).layout().itemAt(0).widget().text()
        i1 = vboxUrlComplex.itemAt(a).layout().itemAt(1).widget().text()
        i2 = vboxUrlComplex.itemAt(a).layout().itemAt(2).widget().text()

        if i0 != "":
            args.append([])
            args[-1].append(i0)
        if i1 != "" and i2 != "":
            args[-1].append(i1)
            args[-1].append(i2)
        a += 1
    return args

def updateTitles ():
    clearLayout(box)

    list = ["memRanobe_MangaLib.json", "memRawWithArgs.json"]
    height = 0

    now = getTime()
    nTime = strptime(now[7:], "%d.%m.%Y")

    for i in list:
        f = open(i, "r")
        memRMLib = json.load(f)

        for book in memRMLib["data"]:
            h = QHBoxLayout()
            # if book["title"] != "":
            lTitle = QLabel(book["title"])
            # lTitle.setMinimumWidth(310)
            lTitle.setMinimumHeight(30)
            lTitle.setMaximumHeight(600)
            lTitle.setWordWrap(True)
            lTitle.adjustSize()
            height += lTitle.height() + 16
            h.addWidget(lTitle, stretch=0)

            # space_ = QLabel()
            # space_.setMinimumWidth(0)

            lUrl = QLabel('<a href="' + book["rawUrl"] + '">' + "Link" + "<\a>")
            lUrl.setOpenExternalLinks(True)
            lUrl.setFixedSize(30,30)
            h.addWidget(lUrl, stretch=1)

            bDelete = QPushButton()
            bDelete.setIcon(QIcon(path("Icons/delete.png")))
            bDelete.setFixedSize(30,30)
            bDelete.setFlat(True)
            bDelete.clicked.connect(lambda l, x=[i, book["title"], book["rawUrl"]] : deleteTitle(x))

            lTime = QLabel()
            was = book["time"]
            wTime = strptime(was, "%H:%M  %d.%m.%Y")
            lTime.setText(was)

            # print(nTime)
            difference = (mktime(nTime) - mktime(wTime)) / 60 / 60
            # print(difference)

            lTime.setStyleSheet("color : grey")
            if difference < 24:
                lTime.setStyleSheet("color : rgb(50,150,50)")
            elif difference < 24*7:
                lTime.setStyleSheet("color : rgb(150,150,50)")


            lTime.setFixedWidth(120)
            h.addWidget(lTime)
            h.addWidget(bDelete)

            box.addLayout(h)
        w1.setFixedHeight(height)
        f.close()

def deleteTitle (input):
    # print(input)
    dialog = QMessageBox()
    dialog.setWindowTitle("Delete title?")
    dialog.setText(input[1])
    dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    dialog.setDefaultButton(QMessageBox.StandardButton.No)
    result = dialog.exec()

    if result == QMessageBox.StandardButton.Yes:
        f = open(input[0], "r")
        j = json.load(f)
        t = 0
        for a in j["data"]:
            if a["rawUrl"] == input[2]:
                del j["data"][t]
                break
            t += 1
        f.close()
        f = open(input[0], "w")
        json.dump(j, f, indent=4)
        f.close()
        updateTitles()

def timerParseAll ():
    # thread = threading.Thread(target=doParseAll)
    # thread.start()
    # thread.join(15)

    out = parseAll()
    labResponse.setText(out[0])
    notify(out[1])

def changeTimeInterval ():
    global interval
    dialog = QInputDialog()
    dialog.setFixedSize(250,200)
    dialog.setWindowTitle("Change Interval")
    dialog.setLabelText("Time Interval:".ljust(45) + "(minutes)")
    dialog.setIntValue(True)
    dialog.setIntRange(10, 10080)
    dialog.setIntValue(interval)

    if dialog.exec() :
        interval = dialog.intValue()
        if interval < 60:
            bTimeSpaces.setText(str(interval) + " minutes")
        elif interval < 24*60:
            bTimeSpaces.setText(str(round(interval/60,2)) + " hours")
        else:
            bTimeSpaces.setText(str(round(interval/60/24,2)) + " days")

def notify (inpText):
    global enableNotify, enableSound
    if enableNotify and inpText != "":
        if enableSound:
            player.play()
        trayIcon.showMessage(inpText, "", QSystemTrayIcon.MessageIcon.NoIcon, 8000)
        # message = QDialog()
        # message.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # messageLayout = QVBoxLayout()
        # message.setLayout(messageLayout)
        #
        # mLabel = QLabel(inpText)
        # mLabel.setMinimumSize(200,50)
        # messageLayout.addWidget(mLabel)
        #
        # h = QHBoxLayout()
        # messageLayout.addLayout(h)
        # space2 = QLabel()
        # h.addWidget(space2)
        # mButton = QPushButton()
        # mButton.setIcon(QIcon(path("Icons/tick.png")))
        # mButton.setFixedSize(30,30)
        # mButton.setFlat(True)
        # mButton.clicked.connect(lambda : message.close())
        # h.addWidget(mButton)
        #
        # message.adjustSize()
        # message.move(QApplication.screens()[0].size().width() - message.width()-50, 50)

        # QTimer.singleShot(8*1000, message.close)
        # message.show()

def clSetNotify ():
    global enableNotify
    enableNotify = not enableNotify
    if enableNotify:
        bPopUpNotice.setIcon(QIcon(path("Icons/pop-up.png")))
    else:
        bPopUpNotice.setIcon(QIcon(path("Icons/pop-up-NO.png")))

def clSetSound ():
    global enableSound
    enableSound = not enableSound
    if enableSound:
        bSoundNotice.setIcon(QIcon(path("Icons/sound.png")))
    else:
        bSoundNotice.setIcon(QIcon(path("Icons/soundNo.png")))

def myResizeEvent (event):
    w1.setFixedWidth(event.size().width() - 40)

def onClose (event):
    event.ignore()
    window.hide()
    trayIcon.showMessage("Приложение работает на фоне", "", QSystemTrayIcon.MessageIcon.Information, 4000)

def onExit ():
    trayIcon.hide()
    QApplication.quit()

def showGuide ():
    guide = QDialog()
    guide.setWindowTitle("SiteInform's Guide")
    guide.setFixedWidth(570)
    guide.resize(570,800)
    guideVbox = QVBoxLayout()

    fG = open(path("guide.md"), "r", encoding="utf-8")
    gText = ""
    for gLine in fG.readlines():
        if gLine[:4] == "<img":
            lst = gLine.find("src=") + 5
            lend = gLine[lst:].find('"') + lst
            newLink = path(gLine[lst:lend])
            gLine = gLine[:lst] + newLink + gLine[lend:]
        gText += gLine
    fG.close()

    gScrollArea = QScrollArea()
    gScrollArea.setWidgetResizable(True)

    labGuide = QLabel(gText)
    font = QFont()
    font.setPointSize(11)

    labGuide.setFont(font)
    labGuide.setTextFormat(Qt.TextFormat.MarkdownText)
    labGuide.setWordWrap(True)
    labGuide.setContentsMargins(10,10,10,10)
    labGuide.setAlignment(Qt.AlignmentFlag.AlignTop)
    gScrollArea.setWidget(labGuide)

    guideVbox.addWidget(gScrollArea)
    guide.setLayout(guideVbox)
    guide.exec()

if __name__ == "__main__":
    app = QApplication (sys.argv)
    app.setWindowIcon(QIcon(path("Icons/appIcon.ico")))
    QApplication.instance().setQuitOnLastWindowClosed(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    # palette = QPalette()

    # Настроим цвета для темной темы
    # palette.setColor(QPalette.ColorRole.Window, QColor(42, 46, 50))  # Цвет фона
    # palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))  # Цвет текста
    # palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))  # Текст на кнопках
    # palette.setColor(QPalette.ColorRole.Base, QColor(27, 30, 32))  # Цвет фона для поля ввода
    # palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(100,100,100))
    # palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 80, 80))
    # palette.setColor(QPalette.ColorRole.Dark, QColor(80, 80, 80))

    # app.setPalette(palette)

    mainFont = QFont()
    mainFont.setPointSize(10)
    app.setFont(mainFont)

    window = QWidget ()
    window.resizeEvent = myResizeEvent
    window.setWindowTitle("SiteNotify")
    # window.setFixedWidth(530)
    window.resize(530,800)

    # Tray mode
    trayIcon = QSystemTrayIcon()
    trayIcon.setIcon(QIcon(path("Icons/appIcon.ico")))
    trayIcon.activated.connect(lambda : window.show())
    trayMenu = QMenu()

    openAction = QAction("Open")
    openAction.triggered.connect(lambda : window.show())
    trayMenu.addAction(openAction)

    exitAction = QAction("Exit")
    exitAction.triggered.connect(lambda : onExit())
    trayMenu.addAction(exitAction)

    trayIcon.setContextMenu(trayMenu)
    trayIcon.show()

    window.closeEvent = onClose
    # -------------------

    fList = ["memRanobe_MangaLib.json", "memRawWithArgs.json"]
    for a in fList:
        try:
            f = open(a, "r")
            f.close()
        except:
            f = open(a, "w")
            f.write('{"data" : []}')
            f.close()

    vbox = QVBoxLayout()
    window.setLayout(vbox)

    player = QSoundEffect()
    player.setSource(QUrl.fromLocalFile(path("Icons/popup-sound.wav")))
    player.setVolume(1)

    # Menu
    menu = QHBoxLayout()
    vbox.addLayout(menu)

    bPopUpNotice = QPushButton()
    bPopUpNotice.setFixedSize(40,40)
    bPopUpNotice.setIcon(QIcon(path("Icons/pop-up.png")))
    bPopUpNotice.setFlat(True)
    bPopUpNotice.clicked.connect(lambda : clSetNotify())
    # bPopUpNotice.clicked.connect(lambda : notify("There is some text")) # For check
    bSoundNotice = QPushButton()
    bSoundNotice.setIcon(QIcon(path("Icons/sound.png")))
    bSoundNotice.setFixedSize(40,40)
    bSoundNotice.setFlat(True)
    bSoundNotice.clicked.connect(lambda : clSetSound())
    bTimeSpaces = QPushButton("30 minutes")
    bTimeSpaces.setIcon(QIcon(path("Icons/timer.png")))
    bTimeSpaces.setFixedSize(120,30)
    bTimeSpaces.setFlat(True)
    bTimeSpaces.clicked.connect(lambda : changeTimeInterval())
    bInform = QPushButton("Guide")
    bInform.clicked.connect(lambda : showGuide())
    bInform.setIcon(QIcon(path("Icons/inform.png")))
    bInform.setFixedSize(80, 30)
    bInform.setFlat(True)
    bUpdateCheck = QPushButton()
    bUpdateCheck.setIcon(QIcon(path("Icons/view.png")))
    bUpdateCheck.setFixedSize(40,40)
    bUpdateCheck.setFlat(True)
    bUpdateCheck.clicked.connect(lambda : checkAllTitles())
    space = QLabel()

    menu.addWidget(bPopUpNotice)
    menu.addWidget(bSoundNotice)
    menu.addWidget(bUpdateCheck)
    menu.addWidget(space)
    menu.addWidget(bTimeSpaces)
    menu.addWidget(bInform)

    # Url input
    hboxUrl = QHBoxLayout()

    urlInputName = QLineEdit()
    urlInputName.setFixedHeight(28)
    urlInputName.setMaximumWidth(286)
    urlInputName.setPlaceholderText("Title")

    vbox.addLayout(hboxUrl)
    vbox.addWidget(urlInputName)

    urlInput = QLineEdit()
    urlInput.setFixedHeight(28)
    urlInput.setPlaceholderText("https://page.with.your.favorite.book")
    urlInput.textChanged.connect(lambda : changedUrl())

    bUrlInp = QPushButton()
    bUrlInp.setFixedSize(30,30)
    bUrlInp.setIcon(QIcon(path("Icons/tick.png")))
    bUrlInp.setFlat(True)
    bUrlInp.clicked.connect(lambda: clUrlSave())

    bUrlLoupe = QPushButton()
    bUrlLoupe.setFixedSize(30,30)
    bUrlLoupe.setIcon(QIcon(path("Icons/loupe.png")))
    bUrlLoupe.setFlat(True)
    bUrlLoupe.clicked.connect(lambda : clLookParse())

    hboxUrl.addWidget(urlInput)
    hboxUrl.addWidget(bUrlInp)
    hboxUrl.addWidget(bUrlLoupe)

    #Url complex abilities
    vboxUrlComplex = QVBoxLayout()
    hboxUrlComplex = QHBoxLayout()

    inputComplex0 = QLineEdit()
    inputComplex0.setFixedHeight(30)
    inputComplex0.setMaximumWidth(160)

    inputComplex1 = QLineEdit()
    inputComplex1.setFixedHeight(30)
    inputComplex1.setMaximumWidth(120)

    inputComplex2 = QLineEdit()
    inputComplex2.setFixedHeight(30)
    inputComplex2.setMaximumWidth(120)

    bInpComplexPlus = QPushButton()
    bInpComplexPlus.setFixedSize(28, 28)
    bInpComplexPlus.setIcon(QIcon(path("Icons/plus.png")))
    bInpComplexPlus.setFlat(True)
    bInpComplexPlus.clicked.connect(lambda : clAddParameter())
    space1 = QLabel()

    hboxUrlComplex.addWidget(inputComplex0)
    hboxUrlComplex.addWidget(inputComplex1)
    hboxUrlComplex.addWidget(inputComplex2)
    hboxUrlComplex.addWidget(bInpComplexPlus)
    hboxUrlComplex.addWidget(space1)

    vboxUrlComplex.addLayout(hboxUrlComplex)
    vbox.addLayout(vboxUrlComplex)

    #Status of request
    labStatus = QLabel()
    labStatus.setStyleSheet("color: rgb(190,190,200)")
    labStatus.setMaximumHeight(0)
    labStatus.setMaximumHeight(90)
    labStatus.setWordWrap(True)
    vbox.addWidget(labStatus)

    #Url response display
    responseArea = QScrollArea()
    responseArea.setWidgetResizable(True)

    labResponse = QLabel()
    labResponse.setStyleSheet("background-color: rgb(38,42,45);")
    labResponse.setContentsMargins(5,5,5,5)
    labResponse.setAlignment(Qt.AlignmentFlag.AlignTop)
    labResponse.setFrameShadow(QFrame.Shadow.Raised)
    responseArea.setWidget(labResponse)
    vbox.addWidget(responseArea,1)

    # filename = os.fspath(CURRENT_DIRECTORY / "htmlFile.html")
    # url = QUrl.fromLocalFile(filename)
    # webWidget = QWebEngineView()
    # webWidget.load(url)
    # webWidget.setMaximumHeight(400)
    # vbox.addWidget(webWidget)

    #List saved Urls
    listArea = QScrollArea()
    box = QVBoxLayout()
    w1= QWidget()

    updateTitles()
    w1.setLayout(box)
    listArea.setWidget(w1)
    vbox.addWidget(listArea,1)

    # Auto checking for updates
    # timer = QTimer()
    # if interval < 10:
    #     interval = 10
    # timer.setInterval(interval*60*1000)
    # timer.timeout.connect(lambda : timerParseAll())
    # timer.start()

    memThread = CheckAllTitlesThread()
    memThread.start()

    window.show()
    sys.exit(app.exec())

# pyinstaller --onefile --windowed file.py
# Сайт с иконками https://icons8.ru/icons/