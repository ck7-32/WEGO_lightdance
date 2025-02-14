import sys
import json
import requests
import netifaces
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget, QFileDialog, QMessageBox, QListWidgetItem

# 掃描區網，找出可能的 ESP32（可改成手動輸入）
def scan_network():
    possible_ips = []
    iface = netifaces.gateways()["default"][netifaces.AF_INET][1]  # 取得網卡名稱
    addrs = netifaces.ifaddresses(iface)
    local_ip = addrs[netifaces.AF_INET][0]['addr']
    base_ip = ".".join(local_ip.split(".")[:3])  # 192.168.1.xxx

    # 嘗試 ping 192.168.1.100~192.168.1.120
    for i in range(100, 120):
        ip = f"{base_ip}.{i}"
        url = f"http://{ip}/"  # 嘗試訪問 ESP32
        try:
            res = requests.get(url, timeout=0.5)
            if res.status_code == 200:
                possible_ips.append(ip)
        except:
            pass

    return possible_ips

# GUI 介面
class ESP32Uploader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESP32 JSON 推送")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("選擇要推送的 ESP32：")
        self.layout.addWidget(self.label)

        self.esp_list = QListWidget()
        self.esp_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  # 可多選
        self.layout.addWidget(self.esp_list)

        self.scan_button = QPushButton("掃描 ESP32")
        self.scan_button.clicked.connect(self.scan_esp)
        self.layout.addWidget(self.scan_button)

        self.file_button = QPushButton("選擇 JSON 檔案")
        self.file_button.clicked.connect(self.select_json)
        self.layout.addWidget(self.file_button)

        self.upload_button = QPushButton("推送 JSON")
        self.upload_button.clicked.connect(self.upload_json)
        self.layout.addWidget(self.upload_button)

        self.setLayout(self.layout)
        self.json_path = None

    def scan_esp(self):
        self.esp_list.clear()
        esp_ips = scan_network()
        for ip in esp_ips:
            item = QListWidgetItem(ip)
            self.esp_list.addItem(item)

    def select_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇 JSON 檔案", "", "JSON Files (*.json)")
        if file_path:
            self.json_path = file_path

    def upload_json(self):
        if not self.json_path:
            QMessageBox.warning(self, "錯誤", "請先選擇 JSON 檔案！")
            return

        selected_items = self.esp_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "錯誤", "請選擇至少一台 ESP32！")
            return

        with open(self.json_path, "r") as f:
            json_data = f.read()

        for item in selected_items:
            esp_ip = item.text()
            url = f"http://{esp_ip}/upload"
            try:
                files = {'file': ('config.json', json_data, 'application/json')}
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    QMessageBox.information(self, "成功", f"成功推送 JSON 至 {esp_ip}")
                else:
                    QMessageBox.warning(self, "失敗", f"ESP32 ({esp_ip}) 回應錯誤: {response.text}")
            except Exception as e:
                QMessageBox.warning(self, "失敗", f"無法連線到 {esp_ip}\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ESP32Uploader()
    window.show()
    sys.exit(app.exec())
