import sys

from PyQt5.QtWidgets import QApplication

import game_process

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = game_process.Game()
    form.show()
    sys.excepthook = game_process.except_hook
    sys.exit(app.exec())
