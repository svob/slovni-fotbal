import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QPoint, Qt, pyqtSlot
from PyQt4.QtGui import *

import gui.Screenshot
from gui import MainWindow
import wordsFinder


class Fotbalek(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Fotbalek, self).__init__(parent)
        self.setupUi(self)

        self.btnLoad.clicked.connect(self.click_loadbtn)
        self.btnDelete.clicked.connect(self.click_deletebtn)

        with open('slovnik.txt', 'r', encoding='utf8') as file:
            self.words = file.read().splitlines()
        self.words.sort(key=len, reverse=True)

    def click_loadbtn(self):
        self.listWidget.clear()
        self.w = gui.Screenshot.ScreenshotWindow()
        self.w.setPixmap(QPixmap.grabWindow(QApplication.desktop().winId()))
        self.w.main_handler = self
        self.w.showFullScreen()

    def click_deletebtn(self):
        print(self.listWidget.takeItem(self.listWidget.currentRow()).text())

    @pyqtSlot()
    def load_pix(handler):
        screen = QtGui.QPixmap('letters.bmp')
        if handler.lblImage.size().width() < screen.size().width() or handler.lblImage.size().height() < screen.size().height():
            screen = screen.scaled(handler.lblImage.size(), Qt.KeepAspectRatio)
        handler.lblImage.setPixmap(screen)
        wf = wordsFinder.WordsFinder()
        for word in handler.words:
            if wf.testWord(word.lower()):
                handler.listWidget.addItem(word)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Fotbalek()
    form.show()
    sys.exit(app.exec_())