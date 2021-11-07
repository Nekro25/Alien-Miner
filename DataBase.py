import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QInputDialog


def show_all(self):
    self.con = sqlite3.connect('Records.sqlite')
    res = self.con.cursor().execute('''SELECT
    players.name, records.steps, records.time, keys."key"
    FROM records
    INNER JOIN players ON players.id = records.name_id
    INNER JOIN keys ON keys.id = records.key_id;''').fetchall()
    self.records_table.setRowCount(0)
    for i, row in enumerate(res):
        self.records_table.setRowCount(
            self.records_table.rowCount() + 1)
        for j, elem in enumerate(row):
            self.records_table.setItem(
                i, j, QTableWidgetItem(str(elem)))


def add_new_player(self, name):
    self.con.cursor().execute(f'''INSERT INTO players(name) VALUES ("{name}")''')
    self.con.commit()


def add_new_key(self, key):
    self.con.cursor().execute(f'''INSERT INTO keys(key) VALUES ("{key}")''')
    self.con.commit()


def add_new_record(self, name, steps, time, key):
    player_id = self.con.cursor().execute(
        f'''SELECT id FROM players WHERE name = "{name}"''').fetchall()[0][0]
    key_id = self.con.cursor().execute(
        f'''SELECT id FROM keys WHERE key = "{key}"''').fetchall()[0][0]
    self.con.cursor().execute(f'''INSERT INTO records(name_id, steps, time, key_id) \
         VALUES ("{player_id}",{steps}, {time}, {key_id})''')
    self.con.commit()


def change_record(self, name, steps, time, key):
    player_id = self.con.cursor().execute(
        f'''SELECT id FROM players WHERE name = "{name}"''').fetchall()[0][0]
    key_id = self.con.cursor().execute(
        f'''SELECT id FROM keys WHERE key = "{key}"''').fetchall()[0][0]
    self.con.cursor().execute(f'''UPDATE records SET time = {time}, steps = {steps} \
             WHERE name_id = {player_id} AND key_id = {key_id}''')
    self.con.commit()


class Winning(QWidget):
    def __init__(self, main, steps, time):
        super().__init__()
        self.main = main
        uic.loadUi('WinForm.ui', self)

        self.steps_lbl.setText(str(steps))
        self.time_lbl.setText(f'{str(time)} sec')

        self.no_btn.clicked.connect(self.cancel)
        self.yes_btn.clicked.connect(self.save_result)

    def save_result(self):
        name, ok_press = QInputDialog.getText(self, 'Name', 'Write your name')
        if ok_press and name:
            exist_player = self.main.con.cursor().execute(
                f'''SELECT id FROM players WHERE name = "{name}"''').fetchall()
            if not exist_player:
                add_new_player(self.main, name)
            exist_player = self.main.con.cursor().execute(
                f'''SELECT id FROM players WHERE name = "{name}"''').fetchall()[0][0]
            exist_key = self.main.con.cursor().execute(
                f'''SELECT id FROM keys WHERE key = "{self.main.key}"''').fetchall()
            if not exist_key:
                add_new_key(self.main, self.main.key)
            exist_key = self.main.con.cursor().execute(
                f'''SELECT id FROM keys WHERE key= "{self.main.key}"''').fetchall()[0][
                0]
            player_rec_time = self.main.con.cursor().execute(
                f'''SELECT time FROM records 
                WHERE name_id = {exist_player} 
                AND key_id = {exist_key}''').fetchall()
            if player_rec_time:
                if player_rec_time[0][0] > self.main.spent_time:
                    change_record(self.main, name, self.main.steps, self.main.spent_time,
                                  self.main.key)
            else:
                add_new_record(self.main, name, self.main.steps, self.main.spent_time,
                               self.main.key)
        show_all(self.main)
        self.close()

    def cancel(self):
        self.close()
