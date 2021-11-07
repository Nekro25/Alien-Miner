
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


def show_all(self):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('records.sqlite')
    db.open()
    model = QSqlTableModel(self, db)
    model.setTable('records')
    model.select()
    self.records_table.setModel(model)