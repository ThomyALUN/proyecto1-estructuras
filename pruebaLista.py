import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Crear una lista de elementos
        self.items = ["Elemento 1", "Elemento 2", "Elemento 3", "Elemento 4"]
        for i in range(20):
            elemento = f"Elemento {i}"
            self.items.append(elemento)

        # Crear un QListWidget
        self.list_widget = QListWidget()

        # Agregar los elementos a la lista
        for item in self.items:
            self.list_widget.addItem(item)

        # Agregar el QListWidget al layout vertical
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())