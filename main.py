import json

from PyQt6.QtCore import QUrl, Qt, QRect, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QScrollArea, QFormLayout, QInputDialog, QMessageBox, QSizePolicy, QDialog
# from PySide6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput

# PySise6 вместо PyQt6, если хочется пользоваться QWebEngineView

import sys
import os
from time import sleep
from pathlib import Path
from parse import parseUrl, lookParse, parseAll

# =======================================

# CURRENT_DIRECTORY = Path(__file__).resolve().parent
interval = 10
enableNotify = True
enableSound = True

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
    bUrlLoupe.setDisabled(True)
    args = getArgs()

    labResponse.setText(lookParse(urlInput.text(), args))

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
    bInpComplexMinus.setIcon(QIcon("Icons/minus.png"))
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
    for i in list:
        f = open(i, "r")
        memRMLib = json.load(f)

        for book in memRMLib["data"]:
            h = QHBoxLayout()
            if book["title"] != "":
                lTitle = QLabel(book["title"])
                lTitle.setMinimumWidth(310)
                lTitle.setMaximumHeight(600)
                lTitle.setWordWrap(True)
                h.addWidget(lTitle, stretch=0)

            space_ = QLabel()
            space_.setMinimumWidth(0)

            lUrl = QLabel('<a href="' + book["rawUrl"] + '">' + "Link" + "<\a>")
            lUrl.setOpenExternalLinks(True)
            lUrl.setFixedSize(30,30)
            h.addWidget(lUrl)

            bDelete = QPushButton()
            bDelete.setIcon(QIcon("Icons/delete.png"))
            bDelete.setFixedSize(30,30)
            bDelete.clicked.connect(lambda l, x=[i, book["title"], book["rawUrl"]] : deleteTitle(x))

            lTime = QLabel()
            lTime.setText(book["time"])
            # lTime.setStyleSheet("color : grey")
            lTime.setFixedWidth(100)
            h.addWidget(lTime)
            h.addWidget(bDelete)

            box.addLayout(h)

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

        timer.setInterval(interval*60*1000)

def notify (inpText):
    global enableNotify, enableSound
    if enableNotify:
        message = QDialog()
        message.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        messageLayout = QVBoxLayout()
        message.setLayout(messageLayout)

        mLabel = QLabel(inpText)
        mLabel.setMinimumSize(200,50)
        messageLayout.addWidget(mLabel)

        h = QHBoxLayout()
        messageLayout.addLayout(h)
        space2 = QLabel()
        h.addWidget(space2)
        mButton = QPushButton()
        mButton.setIcon(QIcon("Icons/tick.png"))
        mButton.setFixedSize(30,30)
        mButton.clicked.connect(lambda : message.close())
        h.addWidget(mButton)

        message.adjustSize()

        message.move(QApplication.screens()[0].size().width() - message.width()-50, 50)
        message.exec()
    if enableSound:
        player.play()

def clSetNotify ():
    global enableNotify
    enableNotify = not enableNotify
    if enableNotify:
        bPopUpNotice.setIcon(QIcon("Icons/pop-up.png"))
    else:
        bPopUpNotice.setIcon(QIcon("Icons/pop-up-NO.png"))

def clSetSound ():
    global enableSound
    enableSound = not enableSound
    if enableSound:
        bSoundNotice.setIcon(QIcon("Icons/sound.png"))
    else:
        bSoundNotice.setIcon(QIcon("Icons/soundNo.png"))


if __name__ == "__main__":
    app = QApplication (sys.argv)
    window = QWidget ()
    window.setWindowTitle("UpdateInform")
    window.setFixedWidth(530)
    window.resize(530,800)

    fList = ["memRanobe_MangaLib.json", "memRawWithArgs.json"]
    for a in fList:
        if not open(a, "r"):
            f = open(a, "w")
            f.write('{"data" : []}')
            f.close()

    vbox = QVBoxLayout()
    window.setLayout(vbox)

    soundFile = "Icons/popup-sound.mp3"
    player = QSoundEffect()
    player.setSource(QUrl.fromLocalFile("Icons/popup-sound.wav"))
    player.setVolume(1)

    # Menu
    menu = QHBoxLayout()
    vbox.addLayout(menu)

    bPopUpNotice = QPushButton()
    bPopUpNotice.setFixedSize(30,30)
    bPopUpNotice.setIcon(QIcon("Icons/pop-up.png"))
    bPopUpNotice.clicked.connect(lambda : clSetNotify())
    bSoundNotice = QPushButton()
    bSoundNotice.setIcon(QIcon("Icons/sound.png"))
    bSoundNotice.setFixedSize(30,30)
    bSoundNotice.clicked.connect(lambda : clSetSound())
    bTimeSpaces = QPushButton("10 minutes")
    bTimeSpaces.setIcon(QIcon("Icons/timer.png"))
    bTimeSpaces.setFixedSize(120,30)
    bTimeSpaces.clicked.connect(lambda : changeTimeInterval())
    bInform = QPushButton("Guide")
    bInform.setIcon(QIcon("Icons/inform.png"))
    bInform.setFixedSize(66, 30)
    space = QLabel()

    menu.addWidget(bPopUpNotice)
    menu.addWidget(bSoundNotice)
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
    bUrlInp.setIcon(QIcon("Icons/tick.png"))
    bUrlInp.clicked.connect(lambda: clUrlSave())

    bUrlLoupe = QPushButton()
    bUrlLoupe.setFixedSize(30,30)
    bUrlLoupe.setIcon(QIcon("Icons/loupe.png"))
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
    bInpComplexPlus.setIcon(QIcon("Icons/plus.png"))
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
    labStatus.setMaximumHeight(0)
    labStatus.setMaximumHeight(90)
    vbox.addWidget(labStatus)

    #Url response display
    responseArea = QScrollArea()
    responseArea.setWidgetResizable(True)

    labResponse = QLabel()
    labStatus.setWordWrap(True)
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
    timer = QTimer()
    if interval < 10:
        interval = 10
    timer.setInterval(interval*60*1000)
    timer.timeout.connect(lambda : timerParseAll())
    timer.start()

    window.show()
    sys.exit(app.exec())

# pyinstaller --onefile --windowed file.py
# Сайт с иконками https://icons8.ru/icons/