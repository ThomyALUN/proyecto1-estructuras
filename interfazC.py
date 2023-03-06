from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi

import sys
class DisenoInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("DiseñoInicio.ui", self)

        # Agregar un botón que muestra la nueva ventana
        self.cerrar.clicked.connect(self.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow   
        self.BIniciar.clicked.connect(self.mostrarVentana1)
        
    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()

    def exit(self):
        app.exit()
        sys.exit()
        
    
        
        
    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()

    def ocultar(self):
        self.close()
    
    def minimizar(self):        
        widget.showMinimized()
        
    def mostrarVentana1(self):
        # Crear una instancia de la nueva ventana
        
        ventana1 = Ventana1()
        ventana1.show()
        
        #self.ocultar()
        

class Ventana1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Ventana1.ui", self)
        
        # Definir la interfaz de usuario de la nueva ventana
        # ...

if __name__ == '__main__':
    app = QApplication([])
    window = DisenoInicio()
    window.show()
    app.exec_()
    