from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel
from UI import Ui_MainWindow
import sys
import os
class CallHandler(QtCore.QObject):
    @QtCore.pyqtSlot(float)
    def receiveTime(self, time):
        print(f"Current time from JavaScript: {time}")
        MainWindow_controller.receivetime(window,time)
        
def getframe(time_segments, current_time):
    left = 0
    right = len(time_segments) - 1

    while left <= right:
        mid = (left + right) // 2
        segment = time_segments[mid]

        if current_time >= segment:
            # If current time is greater than or equal to the segment time, continue searching in the right half
            left = mid + 1
        else:
            # If current time is less than the segment time, continue searching in the left half
            right = mid - 1

    return right

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.html=QtWebEngineWidgets.QWebEngineView(self.ui.html)
        self.html.move(0, 0)
        self.html.resize(930, 510)
        # 確保調用 setup_control 方法
        self.setup_control()
    def setup_control(self):
        #建立嵌入網頁視窗物件
        self.channel = QtWebChannel.QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject("handler", self.handler)
        self.html.page().setWebChannel(self.channel)
        #載入網頁
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, 'index_new.html')
        # 打印路徑以檢查是否正確
        print(f"HTML file path: {html_file_path}")
        self.html.setUrl(QtCore.QUrl.fromLocalFile(html_file_path))

        #按鈕功能綁定
        self.ui.gettime.clicked.connect(self.get_current_time)


        #變數宣告
        self.time=0

    def get_current_time(self):
        self.html.page().runJavaScript('getCurrentTime();')

    def receivetime(self,time):
        self.time=time
        self.ui.nowtime.setText(f"{time}")






if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
