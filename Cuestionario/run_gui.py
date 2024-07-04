import sys
import subprocess
import os
from multiprocessing import Process
from PyQt6.QtCore import QUrl, QDir, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


def run_server():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de Toners")
        self.showMaximized()  # Abrir en pantalla completa

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/datos"))


        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.server_process = None
        self.start_server()  # Iniciar el servidor al abrir la aplicación



    def start_server(self):
        if self.server_process is None:
            self.server_process = Process(target=run_server)
            self.server_process.start()
            print("Servidor Django iniciado, esperando para cargar la URL...")
            QTimer.singleShot(5000, self.load_url)  # Esperar 5 segundos antes de cargar la URL


    def load_url(self):
        print("Cargando URL en el navegador...")
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/datos"))


    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.join()
            self.server_process = None


    def closeEvent(self, event):
        self.stop_server()
        event.accept()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("Aplicación PyQt6 iniciada.")
    sys.exit(app.exec())



