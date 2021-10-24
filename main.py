import sys

from random import randrange
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGame.ui', self)
        self.initUI()

    def initUI(self):
        self.set_btn.clicked.connect(self.settings_set)

    def settings_set(self):
        self.map_size = self.size_dial.value()
        self.map_level = self.level_dial.value()
        self.difficulty = self.difficulty_dial.value() * 3
        self.map = [[0 for i in range(self.map_size ** 2)] for j in range(self.map_level)]



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
