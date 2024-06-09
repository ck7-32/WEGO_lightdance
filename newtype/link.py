from PyQt6 import QtWidgets, QtCore, QtWebEngineWidgets, QtWebChannel
import sys
import os

class CallHandler(QtCore.QObject):
    @QtCore.pyqtSlot(float)
    def receiveTime(self, time):
        print(f"Current time from JavaScript: {time}")

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('oxxo.studio')
        self.resize(800, 600)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.move(0, 0)
        self.browser.resize(800, 600)

        self.channel = QtWebChannel.QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject("handler", self.handler)
        self.browser.page().setWebChannel(self.channel)

        # Use relative path to load the HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.browser.setUrl(QtCore.QUrl.fromLocalFile(os.path.join(current_dir, 'index_new.html')))

        self.button = QtWidgets.QPushButton('Get Current Time', self)
        self.button.move(350, 550)
        self.button.clicked.connect(self.get_current_time)

    def get_current_time(self):
        self.browser.page().runJavaScript('getCurrentTime();')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
