from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel
from UI import Ui_MainWindow
import sys
import os
import json


settingjson_path="setting.json"
datajson_path="data.json"


class CallHandler(QtCore.QObject):
    @QtCore.pyqtSlot(float)
    def receiveTime(self, time):
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
def loadjson(path):
    with open(path, 'r', encoding='utf-8') as file:
        out = json.load(file)
    return out
def savejson(path,data):
    with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
def get_time_index(time_segments, current_time):
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
#初始化
    def setup_control(self):
        #建立嵌入網頁視窗物件
        self.channel = QtWebChannel.QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject("handler", self.handler)
        self.html.page().setWebChannel(self.channel)
        #載入網頁
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, 'index.html')
        # 打印路徑以檢查是否正確
        print(f"HTML file path: {html_file_path}")
        #載入setting.json
        
        self.setting =loadjson(settingjson_path)
        self.data=loadjson(datajson_path)       
        self.html.setUrl(QtCore.QUrl.fromLocalFile(html_file_path))

        #變數宣告
        self.time=0
        self.dancerN=0
        self.nowframe=0
        self.partcolors=[self.ui.color0,self.ui.color1,self.ui.color2,self.ui.color3,self.ui.color4,self.ui.color5,self.ui.color6,self.ui.color7,self.ui.color8,self.ui.color9,self.ui.color10,self.ui.color11]
        self.partlable=[self.ui.part0,self.ui.part1,self.ui.part2,self.ui.part3,self.ui.part4,self.ui.part5,self.ui.part6,self.ui.part7,self.ui.part8,self.ui.part9,self.ui.part10,self.ui.part11]
        self.loaddancer()
        #self.loadcolor()

        #按鈕功能綁定 初始化()
        self.ui.gettime.clicked.connect(self.get_current_time)
        self.ui.settimebtn.clicked.connect(self.settime)
        self.ui.Dancers.addItems(self.setting["dancersname"])
        self.ui.Dancers.currentIndexChanged.connect(self.dancerselected)
        self.ui.save.clicked.connect(self.colorchanged)

#刷新視窗
        
#取得時間
    def get_current_time(self):
        self.html.page().runJavaScript('getCurrentTime();')
#收到時間碼
    def receivetime(self,time):
        if self.time==time:
            pass
        else:
            self.time=time
            self.ui.nowtime.setText(f"{time}")
            self.ui.settime.setText(f"{time}")
            self.nowframe=get_time_index(self.data["frametimes"],self.time*1000)
            self.ui.nowframe.setText(f"{self.nowframe}")
            self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
            self.loaddancer()
#將舞者載入
    def loaddancer(self):
        self.ui.dancernow.setText(self.setting["dancersname"][self.dancerN])
        for i in range(len(self.setting["dancers"][self.dancerN])):
            self.partlable[i].setText(self.setting["dancers"][self.dancerN][i])
        self.loadcolor()


#選擇舞者選單被按下
    def dancerselected(self):
        self.dancerN=self.ui.Dancers.currentIndex()
        self.loaddancer()
    


#設定html視窗內撥放進度的時間
    def settime(self):
        time=self.ui.settime.text()
        print(time)
        self.html.page().runJavaScript(f"setTime({time});")
#儲存setting.json
    def savesetting(self):
        savejson(settingjson_path,self.setting)
        
#快捷鍵
    def keyPressEvent(self, event):
        keycode = event.key()             
        if keycode == 82:
            self.colorchanged()

#載入光效
    def loadcolor(self):
        for i in range(len(self.setting["dancers"][self.dancerN])):
            self.partcolors[i].clear()
            self.partcolors[i].addItems(self.data["colornames"])
            self.partcolors[i].setCurrentIndex(self.data["frames"][self.dancerN][self.nowframe][i])
#顏色被變更
    def colorchanged(self):
        for i in range(len(self.setting["dancers"][self.dancerN])):
            self.data["frames"][self.dancerN][self.nowframe][i]=self.partcolors[i].currentIndex()
        savejson("data.json",self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")





if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())