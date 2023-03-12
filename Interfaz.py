import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QDialog
from imagen import *




class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("DiseñoInicio.ui", self)
        self.cerrar.clicked.connect(self.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow   
        self.BIniciar.clicked.connect(self.iniciarVentana1)     
    
    
        
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
    
    def iniciarVentana1(self):
        ventana1 = Ventana1()
        ventana1.show()
        ventana1.raise_()
        '''widget_2 = QtWidgets.QStackedWidget()
        widget_2.addWidget(ventana1)
        widget_2.setFixedHeight(768)
        widget_2.setFixedWidth(1366)
        widget_2.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        widget_2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        widget_2.show()'''

        
        
class Ventana1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Ventana1.ui", self)
        self.cerrar_2.clicked.connect(WelcomeScreen().ocultar)
        self.min_2.clicked.connect(WelcomeScreen().minimizar)
        self.frame_2.mouseMoveEvent = WelcomeScreen().moveWindow
        
        
        

        
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget_2 = QtWidgets.QStackedWidget()

widget.addWidget(welcome)
widget.setFixedHeight(768)
widget.setFixedWidth(1366)
widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
widget.show()


try: 
    sys.exit(app.exec_())
except:
    print("Saliendo")