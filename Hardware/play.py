import socket
import time
import threading
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

# ESP32 IP地址和端口（示例：假設三個ESP32）
ESP32_1_IP = "192.168.1.200"  # 第一台ESP32的IP地址
ESP32_1_PORT = 12345  # 第一台ESP32接收UDP封包的端口

ESP32_2_IP = "192.168.1.201"  # 第二台ESP32的IP地址
ESP32_2_PORT = 12345  # 第二台ESP32接收UDP封包的端口

ESP32_3_IP = "192.168.1.202"  # 第三台ESP32的IP地址
ESP32_3_PORT = 12345  # 第三台ESP32接收UDP封包的端口

# 時間戳陣列（示例）
timestamp_array = [100, 200, 300, 400]  # 每幀的時間戳

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ESP32控制程式')
        self.setGeometry(100, 100, 300, 200)

        self.start_button = QPushButton('開始', self)
        self.start_button.clicked.connect(self.startTransmission)

        self.frame_label = QLabel('當前幀數: 0', self)
        self.frame_label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.frame_label)

        self.setLayout(vbox)

        self.show()

    def startTransmission(self):
        # 開始廣播時間戳封包的函數
        threading.Thread(target=self.broadcastTimestamp, args=(ESP32_1_IP, ESP32_1_PORT)).start()
        threading.Thread(target=self.broadcastTimestamp, args=(ESP32_2_IP, ESP32_2_PORT)).start()
        threading.Thread(target=self.broadcastTimestamp, args=(ESP32_3_IP, ESP32_3_PORT)).start()

    def broadcastTimestamp(self, esp_ip, esp_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        for idx, timestamp in enumerate(timestamp_array):
            # 準備要廣播的封包內容，這裡假設封包內容為時間戳
            message = str(timestamp).encode('utf-8')

            # 廣播封包到指定的ESP32
            sock.sendto(message, (esp_ip, esp_port))

            # 更新GUI顯示當前幀數
            self.updateFrameLabel(idx + 1)

            # 延遲一段時間，模擬實際應用中的時間間隔
            time.sleep(1)

    def updateFrameLabel(self, frame_number):
        # 在GUI線程中更新當前幀數的函數
        self.frame_label.setText(f'當前幀數: {frame_number}')

    def playMusic(self):
        # 播放音樂的函數
        for filename in os.listdir("【你的名字MAD】前前前世《中日字幕》.mp3"):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                os.system(f'xdg-open {os.path.join("【你的名字MAD】前前前世《中日字幕》.mp3", filename)}')  # 使用系統預設播放器打開音樂文件

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
