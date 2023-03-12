import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,QVBoxLayout, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from imagen import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from manejoDataframe import *
import cv2

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


class Ventana1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Ventana1.ui", self)
        self.setWindowTitle('Ventana 1')
        self.cerrar_2.clicked.connect(window1.exit)
        self.min_2.clicked.connect(self.minimizar)
        self.frame_2.mouseMoveEvent = self.moveWindow
        self.BSubir.clicked.connect(self.seleccionarArchivo)
        self.BReproducir.clicked.connect(self.play)
            
        
        geometry = self.widget.geometry()
        posicion = self.widget.pos()
        print(posicion)
        
        # creamos el nuevo QVideoWidget
        self.videoWidget = QVideoWidget()
        # establecemos la geometría del nuevo QVideoWidget
        self.videoWidget.setGeometry(geometry)
        #Nombre ventana
        self.videoWidget.setWindowTitle("Tutorial")
        self.player = QMediaPlayer(self)
        media = QMediaContent(QUrl.fromLocalFile("Tutorial Google Takeout.mp4"))
        self.player.setMedia(media)
        self.player.setVideoOutput(self.videoWidget)
        

    def seleccionarArchivo(self):
        dirPath = os.getcwd()  # Directorio de la carpeta actual
        # Buscar archivo.csv
        ruta, _ = QFileDialog.getOpenFileName(self, "Buscar Archivo...", "C:\\", "Wanted Files (*.csv)")
        # src = cv2.imread(ruta, cv2.IMREAD_UNCHANGED) #Lee la ruta de la foto
        self.rutaCSV = ruta
        self.controladorDf = ManejoDF(self.rutaCSV)
        #Devuelve la excepción que hay en ManejoDF
        self.mensaje = self.controladorDf.leerCSV(ruta)
        if self.mensaje != None:
            self.mostrarAdvertencia()
            
        else:
           self.mostrarVentana2()
            
            
        print(self.rutaCSV)
        
    
    def minimizar(self):
        self.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def play(self):
        #posición del widget
        self.videoWidget.move(629,120)
        #self.videoWidget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.player.play()
        self.videoWidget.show()   
        
    def mostrarVentana2(self):
        self.ventana2 = Ventana2(self.controladorDf)
        self.ventana2.raise_()
        self.ventana2.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana2.show()
        self.close() 
        self.player.stop()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
        

                    
class Ventana2(QMainWindow):
    def __init__(self,controladorDf):
        super().__init__()
        loadUi("Ventana2.ui", self)
        self.setWindowTitle('Ventana 2')
        self.cerrar_3.clicked.connect(window1.exit)
        self.min_3.clicked.connect(self.minimizar)
        self.frame_3.mouseMoveEvent = self.moveWindow
        self.BCrear.clicked.connect(self.crearEtiqueta)
        self.controladorDf = controladorDf
        #self.BModificar.clicked.connect(self.play)

    def minimizar(self):
        self.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()     
    
    def crearEtiqueta(self):
        DialogEtiquetas(self.controladorDf).show()

                   
class DialogEtiquetas(QDialog):
    def __init__(self,controladorDf):
        super(DialogEtiquetas,self).__init__()
        loadUi("DialogEtiquetas.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.crearEtiqueta)
        
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
        self.showMinimized()
    
    def crearEtiqueta(self):
        self.etiqueta = self.lineEdit.text()
        mensaje = self.controladorDf.crearEtiqueta(self.etiqueta)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
            
                    


        
class Advertencia(QDialog):
    def __init__(self,mensaje):
        super(Advertencia,self).__init__()
        loadUi("Advertencia.ui", self)
        self.cerrar_5.clicked.connect(self.ocultar)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.mouseMoveEvent = self.moveWindow
        self.label_6.setText(mensaje)

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
    