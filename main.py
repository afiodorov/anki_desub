# -*- coding: utf-8 -*-

import os
import sys
import os.path
import PyQt4.QtGui as qg
import PyQt4.QtCore as QtCore
import PIL.Image as image
import widgets
import ocr.tesseract
from translators import bing


def isImage(filepath):
    filename, fileExt = os.path.splitext(filepath)
    return fileExt in ['.jpg', '.png', '.gif']


def getImages(path):
    return filter(isImage, next(os.walk(path))[2])


def resizeImage(imagePath):
    maxWidth, maxHeight = (250, 250)
    imageTempPath = os.path.join('tmp', imagePath)
    try:
        originalImage = image.open(imageTempPath)
    except IOError:
        originalImage = image.open(imagePath)
        width, height = originalImage.size

        if(width > maxWidth):
            scalingFactorW = width / maxWidth
        if(height > maxHeight):
            scalingFactorH = height / maxHeight

        scalingFactor = max(scalingFactorW, scalingFactorH)

        if scalingFactor > 1.0:
            newWidth = width / scalingFactor
            newHeight = height / scalingFactor
            resizedImaged = originalImage.resize((newWidth, newHeight),
                                                 image.ANTIALIAS)
            resizedImaged.save(imageTempPath)

    return imageTempPath


class Window(qg.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initGui()

    def initGui(self):
        layout = qg.QVBoxLayout()

        widget = qg.QWidget()

        for imagePath in getImages('.'):
            resizedImagePath = resizeImage(imagePath)
            flashCard = widgets.ImageText(resizedImagePath)

            try:
                text = ocr.tesseract.recognise(imagePath, '(255, 255, 0)',
                                               'deu')
                flashCard.textFront.setText(text)
                backText = bing.translate(text, 'en', 'de')
                flashCard.textBack.setText(backText)
            except ocr.tesseract.ParsingFailed as e:
                print e
                pass

            layout.addWidget(flashCard)

        quitBtn = qg.QPushButton('Quit', self)
        layout.addWidget(quitBtn)
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quitBtn.resize(quitBtn.sizeHint())

        widget.setLayout(layout)

        scroll = qg.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidget(widget)

        vLayout = qg.QVBoxLayout(self)
        vLayout.addWidget(scroll)

        self.setLayout(vLayout)
        self.resize(800, 800)
        self.setWindowTitle('AnkiDesubber')
        self.show()


application = qg.QApplication(sys.argv)
win = Window()

sys.exit(application.exec_())
