import csv
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QTableView

class CsvTableModel(QAbstractTableModel):
    def __init__(self, csv_file):
        super().__init__()
        self._data = []
        with open(csv_file, "r", newline="",encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._data.append(row)

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        if len(self._data) > 0:
            return len(self._data[0])
        return 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return QVariant(self._data[row][col])
        return QVariant()

if __name__ == "__main__":
    app = QApplication([])
    model = CsvTableModel("suscripciones.csv")
    view = QTableView()
    view.setModel(model)
    view.show()
    app.exec_()