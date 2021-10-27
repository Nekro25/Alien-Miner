import sys

import settings
from random import randrange
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('TheGame.ui', self)
        self.initUI()

    def initUI(self):
        self.set_btn.clicked.connect(self.set_settings)

    def set_settings(self):
        self.map_size = self.size_dial.value()
        self.map_level = self.level_dial.value()
        self.difficulty = self.difficulty_dial.value() * 3
        self.create_map()
        self.show_map(0)

    def create_map(self):
        self.map = [[0 for _ in range(self.map_size ** 2)] for __ in
                    range(self.map_level)]
        for layer_num, layer in enumerate(self.map):
            for cell_num, cell in enumerate(layer):
                if layer_num == 0 and cell_num == 0:
                    self.map[layer_num][cell_num] = settings.Cell('ship')
                elif randrange(100) <= self.difficulty:
                    self.map[layer_num][cell_num] = settings.Cell('lava')
                else:
                    self.map[layer_num][cell_num] = settings.Cell('ground')

    # создает игровую карту

    def show_map(self, layer):
        for num, cell in enumerate(self.map[layer]):
            lbl = QLabel(self)
            if cell.type == 'ship':
                lbl.setPixmap(QPixmap('pictures/ship.png').scaled(500 // self.map_size,
                                                                  500 // self.map_size))
            self.map_layout.addWidget(lbl, num % self.map_size, num // self.map_size)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
