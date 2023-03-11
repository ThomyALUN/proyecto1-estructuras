import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout,QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creamos el reproductor de video
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)

        # Creamos los botones de control
        playButton = QPushButton("Play")
        playButton.clicked.connect(self.play)

        pauseButton = QPushButton("Pause")
        pauseButton.clicked.connect(self.pause)

        stopButton = QPushButton("Stop")
        stopButton.clicked.connect(self.stop)

        # Creamos una etiqueta para mostrar el nombre del archivo
        self.fileLabel = QLabel("No se ha seleccionado ningún archivo de video.")

        # Creamos un layout horizontal para los botones
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(playButton)
        controlLayout.addWidget(pauseButton)
        controlLayout.addWidget(stopButton)

        # Creamos un layout vertical para la ventana principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(videoWidget)
        mainLayout.addWidget(self.fileLabel)
        mainLayout.addLayout(controlLayout)

        # Creamos un widget central para la ventana principal y lo establecemos
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Establecemos el tamaño y título de la ventana principal
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Reproductor de video")

    def play(self):
        # Abrimos un cuadro de diálogo para seleccionar el archivo de video
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de video", "", "Archivos de video (*.mp4 *.avi)")

        if fileName != '':
            # Creamos una instancia de QMediaContent con la URL del archivo de video
            mediaContent = QMediaContent(QUrl.fromLocalFile(fileName))

            # Asignamos la QMediaContent al QMediaPlayer
            self.mediaPlayer.setMedia(mediaContent)

            # Establecemos la etiqueta con el nombre del archivo seleccionado
            self.fileLabel.setText(f"Archivo de video seleccionado: {fileName}")

            # Reproducimos el video
            self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()

    def stop(self):
        self.mediaPlayer.stop()

if __name__ == "__main__":
    # Creamos la aplicación
    app = QApplication(sys.argv)

    # Creamos la ventana principal
    window = MainWindow()
    window.show()

    # Ejecutamos la aplicación
    sys.exit(app.exec_())