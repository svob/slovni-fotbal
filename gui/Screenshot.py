import random, sys
from PyQt4.QtCore import QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt4.QtGui import *
from main import Fotbalek

class ScreenshotWindow(QLabel):
    screenshot_close = pyqtSignal(Fotbalek)
    main_handler = None

    def __init__(self, parent = None):

        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100,100,100,100)
        self.setAutoFillBackground(True)

        self.screenshot_close.connect(Fotbalek.load_pix)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.rubberBand.hide()
        currentQrect = self.rubberBand.geometry()
        cropPixmap = self.pixmap().copy(currentQrect)
        cropPixmap.save('letters.bmp')
        self.close()

    def closeEvent(self, event):
        self.screenshot_close.emit(self.main_handler)