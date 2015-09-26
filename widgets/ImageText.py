import PyQt4.QtGui as qg
import os


class ImageText(qg.QWidget):
    def __init__(self, imagePath):
        super(ImageText, self).__init__()

        layout = qg.QHBoxLayout()

        self.pixmap = qg.QPixmap(os.path.join(os.getcwd(), imagePath))

        label = qg.QLabel(self)
        label.setPixmap(self.pixmap)
        label.resize(self.pixmap.width(), self.pixmap.height())
        layout.addWidget(label)

        textAreas = TwoTextAreas()
        layout.addWidget(textAreas)

        self.textFront = textAreas.textTop
        self.textBack = textAreas.textBottom

        self.setLayout(layout)


class TwoTextAreas(qg.QWidget):
    def __init__(self):
        super(TwoTextAreas, self).__init__()

        layout = qg.QVBoxLayout()

        self.textTop = qg.QTextEdit()
        layout.addWidget(self.textTop)

        self.textBottom = qg.QTextEdit()
        layout.addWidget(self.textBottom)

        self.setLayout(layout)
