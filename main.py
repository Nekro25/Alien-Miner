import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGame.ui', self)
        self.initUI()

    def initUI(self):
        self.bg = QPixmap('BG.png')
        self.background.setPixmap(self.bg)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
