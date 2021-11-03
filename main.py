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
        self.cheat_combo = ''
        self.cc_need = 'upupdwndwnlftrghtlftrghtBA'  # cheat_combination_need
        self.game_going = False
        self.set_btn.clicked.connect(self.set_settings)
        self.up_btn.clicked.connect(self.move_up)
        self.left_btn.clicked.connect(self.move_left)
        self.right_btn.clicked.connect(self.move_right)
        self.down_btn.clicked.connect(self.move_down)
        self.a_btn.clicked.connect(self.dig)
        self.b_btn.clicked.connect(self.check)
        self.c_btn.clicked.connect(self.climb)
        self.d_btn.clicked.connect(self.drop)

    def set_settings(self):
        self.player_cords = [0, 0, 0]
        self.difficulty = self.difficulty_dial.value() * 3
        if self.generate_key.text():
            settings.create_map_by_key(self, self.generate_key.text())
        else:
            self.map_size = self.size_dial.value()
            self.map_level = self.level_dial.value()
            self.create_map()
        self.generate_key.setText(settings.create_key(self.map))
        self.show_map(0)
        self.game_going = True

    def create_map(self):
        self.map = [[0 for _ in range(self.map_size ** 2)] for __ in
                    range(self.map_level)]
        for layer_num, layer in enumerate(self.map):
            for cell_num, cell in enumerate(layer):
                if layer_num == 0 and cell_num == 0:
                    self.map[layer_num][cell_num] = settings.Cell('ship')
                    self.map[layer_num][cell_num] = settings.Cell('ship', player=True)
                elif randrange(100) <= self.difficulty:
                    self.map[layer_num][cell_num] = settings.Cell('lava')
                else:
                    self.map[layer_num][cell_num] = settings.Cell('ground')

    # создает игровую карту

    def show_map(self, layer):
        for i in reversed(range(self.map_layout.count())):  # Удаляет все элементы
            self.map_layout.itemAt(i).widget().setParent(None)  # в layout (нашел в инете)
        for num, cell in enumerate(self.map[layer]):
            lbl = QLabel(self)
            if cell.type == 'ship':
                lbl.setPixmap(QPixmap('pictures/ship.png').scaled(500 // self.map_size,
                                                                  500 // self.map_size))
            elif cell.type == 'lava':
                lbl.setPixmap(QPixmap('pictures/lava.png').scaled(500 // self.map_size,
                                                                  500 // self.map_size))
            self.map_layout.addWidget(lbl, num % self.map_size,
                                      num // self.map_size % self.map_size)
            if cell.up_way:
                lbl.setPixmap(
                    QPixmap('pictures/up_way.png').scaled(500 // self.map_size,
                                                          500 // self.map_size))
                self.map_layout.addWidget(lbl, num % self.map_size,
                                          num // self.map_size % self.map_size)
            if cell.down_way:
                lbl.setPixmap(
                    QPixmap('pictures/down_way.png').scaled(500 // self.map_size,
                                                            500 // self.map_size))
                self.map_layout.addWidget(lbl, num % self.map_size,
                                          num // self.map_size % self.map_size)
        lbl.setPixmap(QPixmap('pictures/man.png').scaled(500 // self.map_size,
                                                         500 // self.map_size))
        self.map_layout.addWidget(lbl, self.player_cords[0], self.player_cords[1])
        # функция addWidget добовляет наоборот - не (х, у), а (у, х),
        # то есть (колонна, строка)

    def move_up(self):
        if self.game_going:
            if self.player_cords[0] != 0:
                self.player_cords[0] -= 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheat_combo += 'up'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'up'
            elif self.cheat_combo == self.cc_need:
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)
        # во всех функциях которым привязаны кнопки действия есть повторяющаяся часть
        # в будущем сделаю для этого отдельную функцию, а сейчас проверял работу чита

    def move_down(self):
        if self.game_going:
            if self.player_cords[0] != self.map_size - 1:
                self.player_cords[0] += 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheat_combo += 'dwn'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'dwn'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)

    def move_left(self):
        if self.game_going:
            if self.player_cords[1] != 0:
                self.player_cords[1] -= 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheat_combo += 'lft'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'lft'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)

    def move_right(self):
        if self.game_going:
            if self.player_cords[1] != self.map_size - 1:
                self.player_cords[1] += 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheat_combo += 'rght'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'rght'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON')
                self.map_layout.addWidget(lbl, 0, 0)

    def dig(self):
        if self.game_going:
            if self.player_cords[2] != self.map_level - 1:
                self.map[self.player_cords[2]][
                    self.player_cords[1] * self.map_size +
                    self.player_cords[0]].down_way = True
                self.map[self.player_cords[2] + 1][
                    self.player_cords[1] * self.map_size +
                    self.player_cords[0]].up_way = True
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.show_map(self.player_cords[2])
            self.cheat_combo += 'A'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'A'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)

    def check(self):
        if self.game_going:
            if self.player_cords[2] != self.map_level - 1:
                if self.map[self.player_cords[2] + 1][
                    self.player_cords[1] * self.map_size + self.player_cords[
                        0]].type == 'lava':
                    self.statusBar().showMessage('Be careful, under of you lava')
                elif self.map[self.player_cords[2] + 1][
                    self.player_cords[1] * self.map_size + self.player_cords[
                        0]].type == 'ore':
                    self.statusBar().showMessage('Good job, you found alien ore!')
                else:
                    self.statusBar().showMessage('It\'s clear, you can dig')
            else:
                self.statusBar().showMessage('You can\'t check under the map')
            self.cheat_combo += 'B'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'B'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)

    def climb(self):
        if self.game_going:
            if self.player_cords[2] != 0:
                self.player_cords[2] -= 1
                self.show_map(self.player_cords[2])
            else:
                self.statusBar().showMessage('You can\'t walk on air')
            self.cheat_combo += 'C'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'C'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)

    def drop(self):
        if self.game_going:
            if self.player_cords[2] != self.map_level - 1:
                self.player_cords[2] += 1
                self.show_map(self.player_cords[2])
            else:
                self.statusBar().showMessage('You can\'t break bedrock')
            self.cheat_combo += 'D'
            if self.cheat_combo not in self.cc_need:
                self.cheat_combo = 'D'
            elif self.cheat_combo == self.cc_need:
                for i in reversed(range(self.map_layout.count())):
                    self.map_layout.itemAt(i).widget().setParent(None)
                self.game_going = False
                lbl = QLabel(self)
                lbl.setText('YOU WON!(You are cheater, it isn\'t interesting)')
                self.map_layout.addWidget(lbl, 0, 0)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
