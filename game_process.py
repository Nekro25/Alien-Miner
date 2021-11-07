import sys

import settings
from constants import *
from DataBase import *
from keyboad import *

from time import time
from random import randrange
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QTabWidget


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/TheGame.ui', self)

        self.cheat_combo = ''
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
        self.keyboard_btn.clicked.connect(self.kb_call)
        self.Game_tabwindow.setCurrentIndex(1)

        user_kb(self)

        show_all(self)

    def keyPressEvent(self, event):
        if event.key() == self.up_kb:
            self.move_up()
        if event.key() == self.down_kb:
            self.move_down()
        if event.key() == self.left_kb:
            self.move_left()
        if event.key() == self.right_kb:
            self.move_right()
        if event.key() == self.A_kb:
            self.dig()
        if event.key() == self.B_kb:
            self.check()
        if event.key() == self.C_kb:
            self.climb()
        if event.key() == self.D_kb:
            self.drop()

    def kb_call(self):
        self.kb_widget = KboardForm(self)
        self.kb_widget.show()

    def set_settings(self):
        self.start_time = time()
        self.player_cords = [0, 0, 0]
        self.got_ore = False
        self.difficulty = self.difficulty_dial.value() * 3
        correct_key = True
        if self.check_key.checkState():
            try:
                settings.create_map_by_key(self, self.generate_key.text())
            except (Exception):
                self.statusBar().showMessage('You should to write correct key')
                correct_key = False
        else:
            self.map_size = self.size_dial.value()
            self.map_level = self.level_dial.value()
            self.create_map()
        if correct_key:
            self.key = settings.create_key(self.map)
            self.generate_key.setText(self.key)
            self.show_map(0)
            self.game_going = True
            self.steps = 0
            self.Game_tabwindow.setCurrentIndex(0)

    def create_map(self):
        self.map = [[0 for _ in range(self.map_size ** 2)] for __ in
                    range(self.map_level)]
        was_ore = False
        add_2 = False
        for layer_num, layer in enumerate(self.map):
            for cell_num, cell in enumerate(layer):
                if not add_2:
                    if layer_num == 0 and cell_num == 0:
                        self.map[layer_num][cell_num] = settings.Cell(SHIP, player=True)
                    elif layer_num == self.map_level - 1 and cell_num == self.map_size ** 2 - 1 and not was_ore:
                        self.map[-1][-1] = settings.Cell(ORE)
                        was_ore = True
                    elif randrange(100) <= self.difficulty:
                        self.map[layer_num][cell_num] = settings.Cell(LAVA)
                        if (not was_ore) and layer_num == self.map_level - 1:
                            self.map[layer_num][cell_num + 1] = settings.Cell(ORE)
                            add_2 = True
                            was_ore = True
                    else:
                        self.map[layer_num][cell_num] = settings.Cell(GROUND)
                else:
                    add_2 = False

    # создает игровую карту

    def show_map(self, layer):
        for i in reversed(range(self.map_layout.count())):  # Удаляет все элементы
            self.map_layout.itemAt(i).widget().setParent(None)  # в layout (нашел в инете)
        for num, cell in enumerate(self.map[layer]):
            lbl = QLabel(self)
            if cell.type == SHIP:
                lbl.setPixmap(QPixmap('pictures/ship.png').scaled(490 // self.map_size,
                                                                  490 // self.map_size))
            elif cell.type == LAVA:
                lbl.setPixmap(QPixmap('pictures/lava.png').scaled(490 // self.map_size,
                                                                  490 // self.map_size))
            elif cell.type == GROUND:
                lbl.setPixmap(QPixmap('pictures/ground.png').scaled(490 // self.map_size,
                                                                    490 // self.map_size))
            self.map_layout.addWidget(lbl, num % self.map_size,
                                      num // self.map_size % self.map_size)
            if cell.up_way:
                lbl = QLabel(self)
                lbl.setPixmap(
                    QPixmap('pictures/up_way.png').scaled(490 // self.map_size,
                                                          490 // self.map_size))
                self.map_layout.addWidget(lbl, num % self.map_size,
                                          num // self.map_size % self.map_size)
            if cell.down_way:
                lbl = QLabel(self)
                lbl.setPixmap(
                    QPixmap('pictures/down_way.png').scaled(490 // self.map_size,
                                                            490 // self.map_size))
                self.map_layout.addWidget(lbl, num % self.map_size,
                                          num // self.map_size % self.map_size)
        lbl = QLabel(self)
        lbl.setPixmap(QPixmap('pictures/man.png').scaled(490 // self.map_size,
                                                         480 // self.map_size))
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
            self.cheating(UP)
            self.lava_burn()
            self.return_with_ore()
            self.steps += 1

    def move_down(self):
        if self.game_going:
            if self.player_cords[0] != self.map_size - 1:
                self.player_cords[0] += 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheating(DOWN)
            self.lava_burn()
            self.return_with_ore()
            self.steps += 1

    def move_left(self):
        if self.game_going:
            if self.player_cords[1] != 0:
                self.player_cords[1] -= 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheating(LEFT)
            self.lava_burn()
            self.return_with_ore()
            self.steps += 1

    def move_right(self):
        if self.game_going:
            if self.player_cords[1] != self.map_size - 1:
                self.player_cords[1] += 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheating(RIGHT)
            self.lava_burn()
            self.return_with_ore()
            self.steps += 1

    def dig(self):
        if self.game_going:
            if self.map[self.player_cords[2]][
                self.player_cords[1] * self.map_size + self.player_cords[
                    0]].type == ORE:
                self.got_ore = True
                self.map[self.player_cords[2]][
                    self.player_cords[1] * self.map_size + self.player_cords[
                        0]].type = GROUND
                self.statusBar().showMessage('Nice, you have ore')
            elif self.player_cords[2] != self.map_level - 1:
                self.map[self.player_cords[2]][
                    self.player_cords[1] * self.map_size +
                    self.player_cords[0]].down_way = True
                self.map[self.player_cords[2] + 1][
                    self.player_cords[1] * self.map_size +
                    self.player_cords[0]].up_way = True
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t break bedrock')
            self.show_map(self.player_cords[2])
            self.cheating(A)
            self.steps += 1

    def check(self):
        if self.game_going:
            if self.map[self.player_cords[2]][
                self.player_cords[1] * self.map_size + self.player_cords[
                    0]].type == ORE:
                self.statusBar().showMessage('Good job, you found alien ore!')
            elif self.player_cords[2] != self.map_level - 1:
                if self.map[self.player_cords[2] + 1][
                    self.player_cords[1] * self.map_size + self.player_cords[
                        0]].type == LAVA:
                    self.statusBar().showMessage('Be careful, under of you lava')
                else:
                    self.statusBar().showMessage('It\'s clear, you can dig')
            else:
                self.statusBar().showMessage('There are no alien ores')
            self.cheating(B)
            self.steps += 1

    def climb(self):
        if self.game_going:
            if self.player_cords[2] != 0 and self.map[self.player_cords[2]][
                self.player_cords[1] * self.map_size + self.player_cords[
                    0]].up_way == True:
                self.player_cords[2] -= 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t walk on air')
            self.cheating(C)
            self.lava_burn()
            self.return_with_ore()
            self.steps += 1

    def drop(self):
        if self.game_going:
            if self.player_cords[2] != self.map_level - 1 and \
                    self.map[self.player_cords[2]][
                        self.player_cords[1] * self.map_size +
                        self.player_cords[0]].down_way == True:
                self.player_cords[2] += 1
                self.show_map(self.player_cords[2])
                self.statusBar().clearMessage()
            else:
                self.statusBar().showMessage('You can\'t go out of the map')
            self.cheating(D)
            self.lava_burn()
            self.steps += 1

    def cheating(self, btn):
        self.cheat_combo += btn
        if self.cheat_combo not in CHEAT_COMBO:
            self.cheat_combo = btn
        elif self.cheat_combo == CHEAT_COMBO:
            self.game_ending('YOU WON!\n(You are cheater, it isn\'t interesting)')

    def game_ending(self, message, win=False):
        self.end_time = time()
        self.spent_time = int(self.end_time - self.start_time)
        for i in reversed(range(self.map_layout.count())):
            self.map_layout.itemAt(i).widget().setParent(None)
        self.game_going = False
        lbl = QLabel(self)
        lbl.setText(message)
        lbl.setFont(QFont('Arial Black', 15))
        self.map_layout.addWidget(lbl, 0, 0)
        if win:
            self.winform = Winning(self, self.steps, self.spent_time)
            self.winform.show()

    def lava_burn(self):
        if self.map[self.player_cords[2]][
            self.player_cords[1] * self.map_size + self.player_cords[
                0]].type == LAVA:
            self.game_ending('Oh no! You burned up in lava')

    def return_with_ore(self):
        if self.player_cords == [0, 0, 0] and self.got_ore:
            self.game_ending('Awesome! You won!', True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
