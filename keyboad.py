from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from constants import *


def user_kb(self):
    file = open(USER_SETTINGS)
    self.us_data = file.readlines()
    self.us_data = [i.split(":") for i in self.us_data]
    self.user_name = self.us_data[0][1]
    self.up_kb = int(self.us_data[1][1])
    self.down_kb = int(self.us_data[2][1])
    self.left_kb = int(self.us_data[3][1])
    self.right_kb = int(self.us_data[4][1])
    self.A_kb = int(self.us_data[5][1])
    self.B_kb = int(self.us_data[6][1])
    self.C_kb = int(self.us_data[7][1])
    self.D_kb = int(self.us_data[8][1])
    file.close()


def write_user_settings(self):
    l = self.us_data[9]  # l - letters
    file = open(USER_SETTINGS, 'w')
    file.write(f'name:{self.user_name}')
    file.write(f'up:{self.up_kb}\n')
    file.write(f'down:{self.down_kb}\n')
    file.write(f'left:{self.left_kb}\n')
    file.write(f'right:{self.right_kb}\n')
    file.write(f'A:{self.A_kb}\n')
    file.write(f'B:{self.B_kb}\n')
    file.write(f'C:{self.C_kb}\n')
    file.write(f'D:{self.D_kb}\n')
    file.write(f'{l[0]}:{l[1]}:{l[2]}:{l[3]}:{l[4]}:{l[5]}:{l[6]}:{l[7]}')
    file.close()


class KboardForm(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        uic.loadUi('Keyboard_settings.ui', self)

        self.user_data = main.us_data

        self.up_btn.clicked.connect(self.up_change)
        self.down_btn.clicked.connect(self.down_change)
        self.left_btn.clicked.connect(self.left_change)
        self.right_btn.clicked.connect(self.right_change)
        self.a_btn.clicked.connect(self.a_change)
        self.b_btn.clicked.connect(self.b_change)
        self.c_btn.clicked.connect(self.c_change)
        self.d_btn.clicked.connect(self.d_change)
        self.apply_btn.clicked.connect(self.apply)

        self.change = False
        self.key_change = UP
        self.show_letters()

    def keyPressEvent(self, event):
        if self.change:
            if self.key_change == UP:
                self.user_data[9][0] = event.text()
                self.user_data[1][1] = str(event.key())
                self.main.up_kb = event.key()
            if self.key_change == DOWN:
                self.user_data[9][2] = event.text()
                self.user_data[2][1] = str(event.key())
                self.main.down_kb = event.key()
            if self.key_change == LEFT:
                self.user_data[9][1] = event.text()
                self.user_data[3][1] = str(event.key())
                self.main.left_kb = event.key()
            if self.key_change == RIGHT:
                self.user_data[9][3] = event.text()
                self.user_data[4][1] = str(event.key())
                self.main.right_kb = event.key()
            if self.key_change == A:
                self.user_data[9][4] = event.text()
                self.user_data[5][1] = str(event.key())
                self.main.a_kb = event.key()
            if self.key_change == B:
                self.user_data[9][5] = event.text()
                self.user_data[6][1] = str(event.key())
                self.main.b_kb = event.key()
            if self.key_change == C:
                self.user_data[9][6] = event.text()
                self.user_data[7][1] = str(event.key())
                self.main.c_kb = event.key()
            if self.key_change == D:
                self.user_data[9][7] = event.text()
                self.user_data[8][1] = str(event.key())
                self.main.d_kb = event.key()
            self.change = False
            self.show_letters()

    def show_letters(self):
        self.up_lbl.setText(self.user_data[9][0])
        self.down_lbl.setText(self.user_data[9][2])
        self.left_lbl.setText(self.user_data[9][1])
        self.right_lbl.setText(self.user_data[9][3])
        self.a_lbl.setText(self.user_data[9][4])
        self.b_lbl.setText(self.user_data[9][5])
        self.c_lbl.setText(self.user_data[9][6])
        self.d_lbl.setText(self.user_data[9][7])

    def apply(self):
        self.main.us_data = self.user_data
        write_user_settings(self.main)
        self.close()

    def up_change(self):
        self.change = True
        self.key_change = UP

    def down_change(self):
        self.change = True
        self.key_change = DOWN

    def left_change(self):
        self.change = True
        self.key_change = LEFT

    def right_change(self):
        self.change = True
        self.key_change = RIGHT

    def a_change(self):
        self.change = True
        self.key_change = A

    def b_change(self):
        self.change = True
        self.key_change = B

    def c_change(self):
        self.change = True
        self.key_change = C

    def d_change(self):
        self.change = True
        self.key_change = D
