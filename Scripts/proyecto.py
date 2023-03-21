import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,QVBoxLayout, QDialog, QListWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from imagen import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from manejoDataframe import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import cv2


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Diseno_interfaz\DiseñoInicio.ui", self)
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
        loadUi("Diseno_interfaz\Ventana1.ui", self)
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
        media = QMediaContent(QUrl.fromLocalFile("Multimedia\Tutorial Google Takeout.mp4"))
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
        loadUi("Diseno_interfaz\Ventana2.ui", self)
        self.cerrar_3.clicked.connect(window1.exit)
        self.min_3.clicked.connect(self.minimizar)
        self.frame_3.mouseMoveEvent = self.moveWindow
        self.BCrear.clicked.connect(self.crearEtiqueta)
        self.BModificar.clicked.connect(self.modificarEtiqueta)
        self.BEliminar.clicked.connect(self.eliminarEtiqueta)
        self.BVer.clicked.connect(self.verEtiquetas)
        self.BSiguiente.clicked.connect(self.mostrarVentana3)
        self.controladorDf = controladorDf
        

    def minimizar(self):
        self.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
            
    def mostrarVentana3(self):
        self.ventana3 = Ventana3(self.controladorDf)
        self.ventana3.raise_()
        self.ventana3.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana3.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana3.show()
        
        self.close()            

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()     
    
    def crearEtiqueta(self):
        CrearEtiqueta(self.controladorDf).show()
        
    def modificarEtiqueta(self):
        ModificarEtiquetas(self.controladorDf).show()
    
    def eliminarEtiqueta(self):
        EliminarEtiqueta(self.controladorDf).show()
    
    def verEtiquetas(self):
        VerEtiquetas(self.controladorDf).show()


class Ventana3(QMainWindow):
    def __init__(self,controladorDf):
        super().__init__()
        loadUi("Diseno_interfaz\Ventana3.ui", self)
        self.cerrar_3.clicked.connect(window1.exit)
        self.min_3.clicked.connect(self.minimizar)
        self.frame_3.mouseMoveEvent = self.moveWindow
        self.BAtras.clicked.connect(self.mostrarVentana2)
        self.BSiguiente.clicked.connect(self.mostrarVentana4)
        self.BClasificar.clicked.connect(self.clasificarCanal)
        self.BRegistrar.clicked.connect(self.registrarCanal)
        self.BEliminar.clicked.connect(self.eliminarCanal)
        self.BModificar.clicked.connect(self.modificarEtqCanal)
        self.BQuitar.clicked.connect(self.quitarEtqCanal)
        self.BConsultar.clicked.connect(self.consultarCanalesEtiquetas)
        self.controladorDf = controladorDf
        self.actualizarListaCanales()
        self.listWidget.itemClicked.connect(self.item_clicked)
        
        
    def minimizar(self):
        self.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mostrarVentana2(self):
        self.ventana2 = Ventana2(self.controladorDf)
        self.ventana2.raise_()
        self.ventana2.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana2.show()
        self.close()
        
    def mostrarVentana4(self):
        self.ventana4 = ExportarArchivo(self.controladorDf)
        self.ventana4.raise_()
        self.ventana4.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana4.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana4.show()
        self.close()
    
    
    def actualizarListaCanales(self):
        self.listWidget.clear()
        self.canales = self.controladorDf.getListaCanales()
        for canal in self.canales:
            self.listWidget.addItem(canal)
    
    def item_clicked(self, item):
        # Obtener el texto del elemento seleccionado
        canal = item.text()
        print(canal)
        VerDatos(self.controladorDf, canal).show()
        
    def clasificarCanal(self):
        ClasificarCanal(self.controladorDf).show()
        
    def registrarCanal(self):
        RegistrarCanal(self.controladorDf,self).show()
    
    def eliminarCanal(self):
        EliminarCanal(self.controladorDf,self).show()
        
    def modificarEtqCanal(self):
        ModificarEtqCanal(self.controladorDf).show()
        
    def quitarEtqCanal(self):
        QuitarEtqCanal(self.controladorDf).show()
    
    def consultarCanalesEtiquetas(self):
        VerEtiquetas(self.controladorDf).show()
     
        
class CrearEtiqueta(QDialog):
    def __init__(self,controladorDf):
        super(CrearEtiqueta,self).__init__()
        loadUi("Diseno_interfaz\CrearEtiqueta.ui", self)
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
        self.lineEdit.clear()
        if mensaje != None:
            #Espacio para que se vea mejor
            mensaje = "      " + mensaje
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = " ¡¡ETIQUETA CREADA CON EXITO!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()
            
                            
class Advertencia(QDialog):
    def __init__(self,mensaje):
        super(Advertencia,self).__init__()
        loadUi("Diseno_interfaz\Advertencia.ui", self)
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

    
class Confirmacion(QDialog):
    def __init__(self,mensaje):
        super(Confirmacion,self).__init__()
        loadUi("Diseno_interfaz\Confirmacion.ui", self)
        self.cerrar_6.clicked.connect(self.ocultar)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.mouseMoveEvent = self.moveWindow
        self.label.setText(mensaje)

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


class ModificarEtiquetas(QDialog):
    def __init__(self,controladorDf):
        super(ModificarEtiquetas,self).__init__()
        loadUi("Diseno_interfaz\ModificarEtiquetas.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.modificarEtiqueta)
        
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
    
    def modificarEtiqueta(self):
        self.oldEtiqueta = self.lineEdit.text()
        self.newEtiqueta = self.lineEdit_2.text()
        mensaje = self.controladorDf.modificarEtiqueta(self.oldEtiqueta,self.newEtiqueta)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        if mensaje != None:
            #Espacio para que se vea mejor
            mensaje = "      " + mensaje
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else: 
            mensaje = "          ¡¡ETIQUETA MODIFICADA!!"
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()


class EliminarEtiqueta(QDialog):
    def __init__(self,controladorDf):
        super(EliminarEtiqueta,self).__init__()
        loadUi("Diseno_interfaz\EliminarEtiqueta.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.eliminarEtiqueta)
        
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
    
    def eliminarEtiqueta(self):
        self.etiqueta = self.lineEdit.text()        
        mensaje = self.controladorDf.eliminarEtiqueta(self.etiqueta)
        self.lineEdit.clear()
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "          ¡¡ETIQUETA ELIMINADA!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()        


class VerEtiquetas(QDialog):

    def __init__(self,controladorDf):
        super(VerEtiquetas,self).__init__()
        loadUi("Diseno_interfaz\VerEtiquetas.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.etiquetas = self.controladorDf.getListaEtiquetas()
        self.listWidget.itemClicked.connect(self.item_clicked)
        print(self.etiquetas)
        for etiqueta in self.etiquetas:
            self.listWidget.addItem(etiqueta)
        

        
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
        
    def item_clicked(self, item):
        # Obtener el texto del elemento seleccionado
        etiqueta = item.text()
        print(etiqueta)
        VerCanales(self.controladorDf, etiqueta).show()
    

class ClasificarCanal(QDialog):

    def __init__(self,controladorDf):
        super(ClasificarCanal,self).__init__()
        loadUi("Diseno_interfaz\ClasificarCanal.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.etiquetas = self.controladorDf.getListaEtiquetas()
        self.BAceptar.clicked.connect(self.clasificarCanal)
        print(self.etiquetas)
        for etiqueta in self.etiquetas:
            self.comboBox.addItem(etiqueta)
        self.comboBox.setCurrentIndex(-1)
             
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

    def clasificarCanal(self):
        self.canal = self.lineEdit.text() 
        self.etiqueta = self.comboBox.currentText()
        mensaje = self.controladorDf.clasificarCanal(self.etiqueta,self.canal)
        self.lineEdit.clear()
        self.comboBox.setCurrentIndex(-1)
        print(mensaje)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "          ¡¡CANAL CLASIFICADO!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()
            
            
class RegistrarCanal(QDialog):
    
    def __init__(self,controladorDf, controladorVentana3):
        super(RegistrarCanal,self).__init__()
        loadUi("Diseno_interfaz\RegistrarCanal.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.registrarCanal)
        self.controladorVentana3 = controladorVentana3
             
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

    def registrarCanal(self):
        self.canal = self.lineEdit.text()
        self.url = self.lineEdit_2.text()
        self.etiqueta = self.lineEdit_3.text()
        if self.etiqueta == "Opcional":
            self.etiqueta = None
        mensaje = self.controladorDf.registrarCanal(self.url,self.canal,self.etiqueta)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        print(mensaje)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "          ¡¡CANAL REGISTRADO!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()
            self.controladorVentana3.actualizarListaCanales()
        
             
class EliminarCanal(QDialog):
    
    def __init__(self,controladorDf,controladorVentana3):
        super(EliminarCanal,self).__init__()
        loadUi("Diseno_interfaz\EliminarCanal.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.eliminarCanal)
        self.controladorVentana3 = controladorVentana3
        
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

    def eliminarCanal(self):
        self.canal = self.lineEdit.text() 
        mensaje = self.controladorDf.eliminarCanal(self.canal)
        self.lineEdit.clear()
        print(mensaje)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "          ¡¡CANAL ELIMINADO!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()
            self.controladorVentana3.actualizarListaCanales()


class ModificarEtqCanal(QDialog):
    
    def __init__(self,controladorDf):
        super(ModificarEtqCanal,self).__init__()
        loadUi("Diseno_interfaz\ModificarEtqCanal.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.etiquetas = self.controladorDf.getListaEtiquetas()
        self.BAceptar.clicked.connect(self.modificarEtqCanal)
        print(self.etiquetas)
        for etiqueta in self.etiquetas:
            self.comboBox.addItem(etiqueta)
        self.comboBox.setCurrentIndex(-1)
             
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

    def modificarEtqCanal(self):
        self.canal = self.lineEdit.text() 
        self.nuevaEtiqueta = self.comboBox.currentText()
        mensaje = self.controladorDf.modificarEtqCanal(self.nuevaEtiqueta,self.canal)
        self.lineEdit.clear()
        self.comboBox.setCurrentIndex(-1)
        print(mensaje)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "          ¡¡CANAL MODIFICADO!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()


class QuitarEtqCanal(QDialog):
    
    def __init__(self,controladorDf):
        super(QuitarEtqCanal,self).__init__()
        loadUi("Diseno_interfaz\QuitarEtqCanal.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.BAceptar.clicked.connect(self.quitarEtqCanal)
        
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

    def quitarEtqCanal(self):
        self.canal = self.lineEdit.text() 
        mensaje = self.controladorDf.quitarEtqCanal(self.canal)
        self.lineEdit.clear()
        print(mensaje)
        if mensaje != None:
            self.advertencia = Advertencia(mensaje)
            self.advertencia.show()
        else:
            mensaje = "   ¡¡CANAL SIN ETIQUETA!!" 
            self.confirmacion = Confirmacion(mensaje)
            self.confirmacion.show()


class VerDatos(QDialog):
    
    def __init__(self,controladorDf,canal):
        super(VerDatos,self).__init__()
        loadUi("Diseno_interfaz\VerDatos.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.canal = canal
        self.verDatos()
        
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

    def verDatos(self):
        datos = self.controladorDf.getDatosCanal(self.canal) 
        self.label_4.setText(self.canal)
        # Establecer la propiedad openExternalLinks en True
        self.label_5.setOpenExternalLinks(True)
        
        #for dato in datos:
        self.url = datos[0]
        self.etiqueta = datos[1]                                                                                                
        self.label_5.setText(self.url)
        self.label_5.setText(f'<a href="{self.url}">{self.url}</a>')
        self.label_6.setText(self.etiqueta)    
        

class VerCanales(QDialog):
    
    def __init__(self,controladorDf,etiqueta):
        super(VerCanales,self).__init__()
        loadUi("Diseno_interfaz\VerCanales.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.etiqueta = etiqueta
        self.verCanales()
        self.listWidget.itemClicked.connect(self.item_clicked)       
        
               
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

    def verCanales(self):
        self.canales = self.controladorDf.getCanalesEtiqueta(self.etiqueta) 
        for canal in self.canales:
            self.listWidget.addItem(canal)
        
    def item_clicked(self, item):
        # Obtener el texto del elemento seleccionado
        canal = item.text()
        print(canal)
        VerDatos(self.controladorDf, canal).show()            
        

class ConsultarEtiquetas(QDialog):
    
    def __init__(self,controladorDf):
        super(ConsultarEtiquetas,self).__init__()
        loadUi("Diseno_interfaz\ConsultarEtiquetas.ui", self)
        self.cerrar_4.clicked.connect(self.ocultar)
        self.min_4.clicked.connect(self.minimizar)
        self.frame_4.mouseMoveEvent = self.moveWindow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.controladorDf = controladorDf
        self.etiquetas = self.controladorDf.getListaEtiquetas()
        print(self.etiquetas)
        for etiqueta in self.etiquetas:
            self.listWidget.addItem(etiqueta)
        
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


class ExportarArchivo(QMainWindow):
    def __init__(self,controladorDf):
        super(ExportarArchivo,self).__init__()
        loadUi("Diseno_interfaz\ExportarArchivo.ui", self)
        self.cerrar_3.clicked.connect(self.exit)
        self.min_3.clicked.connect(self.minimizar)
        self.frame_3.mouseMoveEvent = self.moveWindow
        self.BExportar.clicked.connect(self.exportarArchivo)
        self.controladorDf = controladorDf
        
        
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

    def exportarArchivo(self):
        #Navegador de archivos
        file_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta donde guardar archivo")
        if file_path:
            nombre_archivo = "CanalesClasificados.csv"
            ruta_guardado = os.path.join(file_path, nombre_archivo)
            self.controladorDf.crearCSV(ruta_guardado)
            
        
        

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
    