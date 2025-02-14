import sys
import socket
import threading
from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel,QtGui
from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QShortcut,QStandardItemModel, QStandardItem,QColor , QPalette
from PyQt6.QtCore import Qt,QTimer
from managerUI import Ui_MainWindow


class ESP32Scanner:
    def __init__(self):
        self.devices = []
        self.scan_network()
    
    def scan_network(self):
        self.devices = []
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(2)
        message = b"DISCOVER_ESP32"
        udp_socket.sendto(message, ('<broadcast>', 8266))
        try:
            while True:
                data, addr = udp_socket.recvfrom(1024)
                if data.decode() == "ESP32_RESPONSE":
                    self.devices.append(addr[0])
        except socket.timeout:
            pass
        udp_socket.close()

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
