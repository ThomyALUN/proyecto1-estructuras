import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from imagen import *
from PyQt5 import QtCore, QtGui, QtWidgets 

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("DiseñoInicio.ui", self)
        self.cerrar.clicked.connect(self.exit)
        self.min.clicked.connect(self.minimizar)
        self.setWindowTitle('Ventana Inicio')
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
    
    def minimizar(self):        
        widget.showMinimized()

    def mostrarVentana1(self):
        self.ventana1 = Ventana1()
        self.ventana1.raise_()
        self.ventana1.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana1.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana1.show()
        
        self.close()
        '''self.widget_2 = QtWidgets.QStackedWidget()
        self.widget_2.addWidget(self.ventana1)
        self.widget_2.setFixedHeight(widget.height())  # Configurar el mismo alto que widget
        self.widget_2.setFixedWidth(widget.width())   # Configurar el mismo ancho que widget

        self.widget_2.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget_2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget_2.show()  # Agregar esta línea para mostrar el QStackedWidget'''

class Ventana1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Ventana1.ui", self)
        self.setWindowTitle('Ventana 1')
        self.cerrar_2.clicked.connect(window1.exit)
        self.min_2.clicked.connect(self.minimizar)
        self.frame_2.mouseMoveEvent = self.moveWindow
        
    def minimizar(self):        
        self.showMinimized()
    
    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
            
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1 = Window1()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(window1)
    widget.setFixedHeight(768)
    widget.setFixedWidth(1366)
    widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    widget.show()
    
    window1.show()
    sys.exit(app.exec_())
    