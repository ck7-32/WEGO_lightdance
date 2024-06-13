import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class ColorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data(Qt.ItemDataRole.DisplayRole)
        color = index.data(Qt.ItemDataRole.UserRole)

        painter.save()

        # Draw background if the item is selected
        if option.state & QStyleOptionViewItem.State.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Draw the text with the specified color
        if color:
            painter.setPen(QColor(color))
        else:
            painter.setPen(option.palette.text().color())

        painter.drawText(option.rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
        painter.restore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItem("Red")
        self.comboBox.addItem("Green")
        self.comboBox.addItem("Blue")

        # Set custom colors for each item
        self.comboBox.setItemData(0, "red", Qt.ItemDataRole.UserRole)
        self.comboBox.setItemData(1, "green", Qt.ItemDataRole.UserRole)
        self.comboBox.setItemData(2, "blue", Qt.ItemDataRole.UserRole)

        # Set the custom delegate
        self.comboBox.setItemDelegate(ColorDelegate())

        layout.addWidget(self.comboBox)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
