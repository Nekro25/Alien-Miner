from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class KboardForm(QWidget):
    def __init__(self, main):
        super().__init__()
        main = main
        uic.loadUi('Keyboard_settings.ui', self)
