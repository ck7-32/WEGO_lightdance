from PyQt6 import QtWidgets, QtGui,QtCore, QtWebEngineWidgets, QtWebChannel
from UI import Ui_MainWindow
import sys
import os
class CallHandler(QtCore.QObject):
    @QtCore.pyqtSlot(float)
    def receiveTime(self, time):
        print(f"Current time from JavaScript: {time}")


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.html=QtWebEngineWidgets.QWebEngineView(self.ui.centralwidget)
        self.ui.html.setGeometry(QtCore.QRect(20, 10, 961, 521))
        self.ui.html.setObjectName("html")
    def setup_control(self):
        self.channel = QtWebChannel.QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject("handler", self.handler)

        self.ui.html.setPage(QtWebEngineWidgets.QWebEnginePage(self.ui.html))
        self.ui.html.page().setWebChannel(self.channel)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui.html.setUrl(QtCore.QUrl.fromLocalFile(os.path.join(current_dir, 'index_new.html')))

        self.ui.loadtime.clicked.connect(self.get_current_time)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
