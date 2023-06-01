#python 3.11.1
import socket
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QLabel, QVBoxLayout
import pickle as pik
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QPushButton, QDialog, QRadioButton, QLabel, QLineEdit,QListWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QTimer
from PyQt5 import QtGui
from threading import Thread as thd
from PyQt6.QtCore import QThread, pyqtSignal
import time


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        # создаем три макета
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        
        
        
        #кнопки наверху чтобы они в рот сослись!
        self.btn1 = QPushButton('Новый Чат')
        self.btn3 = QPushButton('Send')
        self.btn3.clicked.connect(self.send)                
        layout1.addWidget(self.btn1)
        layout1.addWidget(self.btn3)

        
        # global нужен для того, чтобы вынести переменную в глобальную область видимости
        global text_field
        # а дальше всё как обычно
        text_field = QTextEdit(self)
        text_field.setReadOnly(True)
        # задаем размер текстового поля
        text_field.setFixedSize(200, 500)  
        layout2.addWidget(text_field)
        

        
        # добавляем виджеты в первый макет
        layout1.addWidget(QWidget())
        layout1.addWidget(QWidget())
        
        # добавляем виджеты во второй макет
        layout2.addWidget(QWidget())
        layout2.addWidget(QWidget())
        layout2.addWidget(QWidget())
        
        # добавляем виджеты в третий макет
        layout3.addWidget(QWidget())
        layout3.addWidget(QWidget())
        layout3.addWidget(QWidget())
        
        # создаем сплиттер и добавляем три макета
        splitter = QSplitter()
        splitter.addWidget(QWidget())
        splitter.addWidget(QWidget())
        splitter.addWidget(QWidget())
        
        # устанавливаем каждый макет в сплиттер
        splitter.widget(0).setLayout(layout1)
        splitter.widget(1).setLayout(layout2)
        splitter.widget(2).setLayout(layout3)
        
        # устанавливаем сплиттер как макет окна
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def send(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")            

class WorkerThread(QThread):
    finished = pyqtSignal() # сигнал, который будет отправлен после выполнения

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    text_field.append(data.decode("utf-8"))    
        

app = QApplication(sys.argv)
# А дальше всё как обычно
window = Window()
# А дальше всё как обычно
worker = WorkerThread()
worker.start()
window.show()
sys.exit(app.exec_())
