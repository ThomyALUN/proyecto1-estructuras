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
        self.min.clicked.connect(self.mini)
        self.frame.mouseMoveEvent = self.moveWindow        
    
    
        
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
    
    def mini(self):        
        widget.showMinimized()
        
class VentanaEnviar(QDialog):
    def __init__(self,placa,municipio,respuesta):
        super(VentanaEnviar,self).__init__()
        loadUi("VentanaEnviar.ui", self)
        self.cerrar_5.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_2.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget_2 = QtWidgets.QStackedWidget()

widget.addWidget(welcome)
widget.setFixedHeight(5600)
widget.setFixedWidth(10400)
widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
widget.show()


try: 
    sys.exit(app.exec_())
except:
    print("Saliendo")