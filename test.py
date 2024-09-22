import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QComboBox Color Example")
        self.setGeometry(100, 100, 300, 200)

        # 顏色陣列
        self.colors = ["#000000", "#269aff", "#ffffff", "#faff95", "#ff67b8", "#ff9d9f", 
                       "#ffa5ff", "#d9aeff", "#8ac8ff", "#82f3ff", "#97ffac", "#f5ff9e", "#ff8181"]

        # 創建 QComboBox
        self.combo_box = QComboBox()

        # 創建標準模型
        model = QStandardItemModel()

        # 將顏色和對應的項目添加到模型中
        for color in self.colors:
            item = QStandardItem()
            item.setText(color)
            item.setBackground(QColor(color))  # 設置每個項目的背景顏色
            model.appendRow(item)

        # 將模型設置到 combo_box
        self.combo_box.setModel(model)

        # 連接信號，當索引改變時更新顯示框的背景顏色
        self.combo_box.currentIndexChanged.connect(self.update_combobox_background)

        # 初始化，設置當前索引為 0 的背景顏色
        self.update_combobox_background(0)

        # 設置佈局
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 設置樣式表來禁用懸浮和選中時的高亮效果
        self.combo_box.setStyleSheet("""
            QComboBox QAbstractItemView::item:hover {
                background-color: none;  /* 禁用懸浮效果的高亮 */
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: none;  /* 禁用選中項目的高亮 */
            }
        """)

    def update_combobox_background(self, index):
        # 根據當前索引設置 combo_box 顯示框的背景顏色
        selected_color = self.colors[index]
        
        # 使用 palette 設置編輯區域的背景顏色
        palette = self.combo_box.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(selected_color))  # 設置 QComboBox 顯示框的背景顏色
        self.combo_box.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
