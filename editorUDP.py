from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel,QtGui
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtGui import QColor 
from UI import Ui_MainWindow
import sys
import os
import json
import time as la
import socket
import struct

settingjson_path="setting.json"
datajson_path="data.json"
#我打算讓他editor附上udp的功能
# 設定廣播地址和埠
broadcast_address = '255.255.255.255'
broadcast_port = 12345

# 創建 UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def UDP(nowframe):
    message = struct.pack('>i', nowframe)
    sock.sendto(message, (broadcast_address, broadcast_port))

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
            json.dump(data, file, ensure_ascii=False)
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



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
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
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
        self.html.setUrl(QtCore.QUrl("http://127.0.0.1:5500/index.html"))

        #變數宣告
        self.time=0
        self.dancerN=0
        self.nowframe=0
        self.partcolors=[self.ui.color0,self.ui.color1,self.ui.color2,self.ui.color3,self.ui.color4,self.ui.color5,self.ui.color6,self.ui.color7,self.ui.color8,self.ui.color9,self.ui.color10,self.ui.color11,self.ui.color12,self.ui.color13,self.ui.color14,self.ui.color15,self.ui.color16,self.ui.color17]
        self.partlable=[self.ui.part0,self.ui.part1,self.ui.part2,self.ui.part3,self.ui.part4,self.ui.part5,self.ui.part6,self.ui.part7,self.ui.part8,self.ui.part9,self.ui.part10,self.ui.part11,self.ui.part12,self.ui.part13,self.ui.part14,self.ui.part15,self.ui.part16,self.ui.part17]
        self.loaddancer()
        self.partnum=0
        #self.loadcolor()

        #按鈕功能綁定 初始化()
        self.ui.settimebtn.clicked.connect(self.settime)
        self.ui.Dancers.addItems(self.setting["dancersname"])
        self.ui.Dancers.currentIndexChanged.connect(self.dancerselected)
        self.ui.save.clicked.connect(self.colorchanged)
        self.ui.savepreset.clicked.connect(self.save_as_preset)
        self.ui.loadpreset.clicked.connect(self.loadpreset)
        self.ui.delpreset.clicked.connect(self.delpreset)
        self.ui.nowframe.setText(f"{self.nowframe}")
        self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
        self.loaddancer()
        self.reloadpresets()
        self.ui.set_frame_start_bynowtime.clicked.connect(self.set_frame_start_bynowtime)
        self.ui.set_frame_end_bynowtime.clicked.connect(self.set_frame_end_bynowtime)
        self.ui.newframe.clicked.connect(self.addnewframe)
        self.ui.delframe.clicked.connect(self.delframe)
        self.ui.delcolor.clicked.connect(self.delcolor)
        self.ui.loadframestarttime.clicked.connect(self.setframestarttime)
        self.loadcolors()
        self.ui.addcolor.clicked.connect(self.addnewcolor)
        self.ui.editcolor.clicked.connect(self.editcolor)
        self.ui.renamecolor.clicked.connect(self.editcolorname)
        self.ui.showcolor.clicked.connect(self.colorpreview)
        self.ui.colors.currentIndexChanged.connect(self.colorpreview)
        #設置全局快捷鍵
        self.shortcut_colorchanged = QShortcut(QtGui.QKeySequence("1"), self)
        self.shortcut_colorchanged.activated.connect(self.colorchanged)
        self.shortcut_set_frame_start = QShortcut(QtGui.QKeySequence("2"), self)
        self.shortcut_set_frame_start.activated.connect(self.set_frame_start_bynowtime)
        self.shortcut_set_frame_end = QShortcut(QtGui.QKeySequence("3"), self)
        self.shortcut_set_frame_end.activated.connect(self.set_frame_end_bynowtime)
        self.shortcut_play_pause = QShortcut(QtGui.QKeySequence("G"), self)
        self.shortcut_play_pause.activated.connect(lambda: self.html.page().runJavaScript("wavesurfer.playPause()"))
        self.shortcut_add_frame = QShortcut(QtGui.QKeySequence("A"), self)
        self.shortcut_add_frame.activated.connect(self.addnewframe)
        self.shortcut_del_frame = QShortcut(QtGui.QKeySequence("D"), self)
        self.shortcut_del_frame.activated.connect(self.delframe)
        self.shortcut_forward=QShortcut(QtGui.QKeySequence("P"), self)
        self.shortcut_forward.activated.connect(self.forward)
        self.shortcut_backward=QShortcut(QtGui.QKeySequence("O"), self)
        self.shortcut_backward.activated.connect(self.backward)
        self.shortcut_zoomin=QShortcut(QtGui.QKeySequence("9"),self)
        self.shortcut_zoomin.activated.connect(self.zoomin)
        self.shortcut_zoomout=QShortcut(QtGui.QKeySequence("8"),self)
        self.shortcut_zoomout.activated.connect(self.zoomout)
        self.shortcut_scrollleft=QShortcut(QtGui.QKeySequence("-"),self)
        self.shortcut_scrollleft.activated.connect(self.scrollleft)
        self.shortcut_scrollright=QShortcut(QtGui.QKeySequence("="),self)
        self.shortcut_scrollright.activated.connect(self.scrollright)


#刷新視窗
        
#收到時間碼
    def receivetime(self,time):
        if self.time==time:
            return
        
        self.time=time
        self.ui.nowtime.setText(f"{time}")
        self.ui.settime.setText(f"{time}")
        frame=get_time_index(self.data["frametimes"],self.time*1000)
        if self.nowframe==frame:
            return
        self.nowframe=frame
        UDP(frame)
        self.ui.nowframe.setText(f"{self.nowframe}")
        self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
        self.loaddancer()
#將舞者載入
    def loaddancer(self):
        self.ui.dancernow.setText(self.setting["dancersname"][self.dancerN])
        self.partnum=len(self.setting["dancers"][self.dancerN])
        for i in range(self.partnum):
            self.partlable[i].show()
            self.partcolors[i].show()
            self.partlable[i].setText(self.setting["dancers"][self.dancerN][i])
        for i in range(18-self.partnum):
            self.partlable[17-i].hide()
            self.partcolors[17-i].hide()
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
   
    def setframestarttime(self):
        time=self.data["frametimes"][self.nowframe]/1000
        print(time)
        self.html.page().runJavaScript(f"setTime({time});")
#儲存setting.json
    def savesetting(self):
        savejson(settingjson_path,self.setting)
        

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
        print(f"第{self.nowframe}幀已改變")
        savejson("data.json",self.data)
        
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#save as preset
    def save_as_preset(self):
        name=self.ui.presetname.text()
        print("1")
        if name =="":
            QtWidgets.QMessageBox.information(self, '警告', '輸入框不能為空')
            return
        elif name in self.setting["presetnames"]:
            QtWidgets.QMessageBox.information(self, '警告', '輸入框不能為空')
            return
       
        preset=[]
        for i in range(self.partnum):
            preset.append(self.partcolors[i].currentIndex())
        self.setting["presets"].append(preset)
        self.setting["presetnames"].append(name)
        savejson(settingjson_path,self.setting)
        self.reloadpresets()
       # self.ui.presets.setItemData((len(self.setting["presetnames"]))-1)
#load preset
    def loadpreset(self):
        index=self.ui.presets.currentIndex()
        for i in range(len(self.setting["dancers"][self.dancerN])):
            self.partcolors[i].setCurrentIndex(self.setting["presets"][index][i])
        self.colorchanged()
#del preset
    def delpreset(self):
        index=self.ui.presets.currentIndex()
        del self.setting["presets"][index]
        del self.setting["presetnames"][index]
        savejson(settingjson_path,self.setting)
        self.reloadpresets()
#reload presets
    def reloadpresets(self):
        self.ui.presets.clear()
        self.ui.presets.addItems(self.setting["presetnames"])

#更改當前幀開始時間
    def set_frame_start_bynowtime(self):
        time=self.time*1000
        if self.nowframe==0:
            QtWidgets.QMessageBox.information(self, '警告', '不能調整第一幀開始時間')
            return
        if time == None:
            time=self.time
        if self.data["frametimes"][self.nowframe-1] > time:
            QtWidgets.QMessageBox.information(self, '警告', '調整後的時間不能超過前一幀')
            return
        elif self.nowframe< len(self.data["frametimes"])-1 :
            if self.data["frametimes"][self.nowframe+1] < time:
                QtWidgets.QMessageBox.information(self, '警告', '調整後的時間不能超過後一幀')
                return
        self.data["frametimes"][self.nowframe]=time
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#當前時間設為當前偵開始時間
    def set_frame_end_bynowtime(self):
        time=self.time*1000
        if self.data["frametimes"][self.nowframe] > time:
            QtWidgets.QMessageBox.information(self, '警告', '調整後的時間不能超過開始時間')
            return
        elif self.nowframe==len(self.data["frametimes"])-1 :
            QtWidgets.QMessageBox.information(self, '警告', '請先新增下一幀的開始時間')
            return
        elif self.nowframe<len(self.data["frametimes"])-2 :
            if self.data["frametimes"][self.nowframe+2] < time:
                QtWidgets.QMessageBox.information(self, '警告', '調整後的時間不能超過後一幀的結束時間')
                return
        self.data["frametimes"][self.nowframe+1]=time
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#新增關鍵幀
    def addnewframe(self):
        if self.data["frametimes"][self.nowframe]==self.time*1000:
             QtWidgets.QMessageBox.information(self, '警告', '與當前幀重疊')
             return
        for i in range(len(self.data["frames"])):
            self.data["frames"][i].insert(self.nowframe+1,self.data["frames"][i][self.nowframe])
        self.data["frametimes"].insert(self.nowframe+1,self.time*1000)
        savejson("data.json",self.data)
        self.nowframe+=1
        self.ui.nowframe.setText(f"{self.nowframe}")
        self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
        self.data=loadjson(datajson_path)
#刪除關鍵幀
    def delframe(self):
        if self.nowframe==0:
            QtWidgets.QMessageBox.information(self, '警告', '不能刪除第一幀')
            return
        for i in range(len(self.data["frames"])):
            del self.data["frames"][i][self.nowframe]
        del self.data["frametimes"][self.nowframe]
        savejson("data.json",self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#載入顏色到上方選項
    def loadcolors(self):
        self.ui.colors.clear()
        self.ui.colors.addItems(self.data["colornames"])
#刪除該顏色
    def delcolor(self):
        index=self.ui.colors.currentIndex()
        if index==0:
            QtWidgets.QMessageBox.information(self, '警告', '不能刪除黑色')
            return
        del self.data["color"][index]
        del self.data["colornames"][index]
        for dN in range(len(self.data["frames"])):
            for fN in range(len(self.data["frames"][dN])):
                for parts in range(len(self.data["frames"][dN][fN])):
                    if self.data["frames"][dN][fN][parts]==index:
                        self.data["frames"][dN][fN][parts]=0
                    elif self.data["frames"][dN][fN][parts]>index:
                        self.data["frames"][dN][fN][parts]-=1
        savejson(datajson_path,self.data)
        self.loaddancer()
        self.loadcolor()
        self.loadcolors()
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#新增顏色
    def addnewcolor(self):
        colorname=self.ui.colorname.text()
        if colorname in self.data["colornames"]:
            QtWidgets.QMessageBox.information(self, '警告', '顏色名稱重疊')
            return
        if colorname=="":
            QtWidgets.QMessageBox.information(self, '警告', '顏色名稱不能為空白')
            return
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.data["color"].append(col.name())
            self.data["colornames"].append(colorname)
            savejson(datajson_path,self.data)
            self.loaddancer()
            self.loadcolor()
            self.loadcolors()
            self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#編輯顏色    
    def editcolor(self):
        index=self.ui.colors.currentIndex()
        if index==0:
            QtWidgets.QMessageBox.information(self, '警告', '不能編輯黑色')
            return
        initial_color = QColor(self.data["color"][index])
        col = QtWidgets.QColorDialog.getColor(initial=initial_color)
        if col.isValid():
            self.data["color"][index]=col.name()
            savejson(datajson_path,self.data)
            self.loaddancer()
            self.loadcolor()
            self.loadcolors()
            self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#編輯顏色名稱
    def editcolorname(self):
        colorname=self.ui.colorname.text()
        index=self.ui.colors.currentIndex()
        if colorname in self.data["colornames"]:
            QtWidgets.QMessageBox.information(self, '警告', '顏色名稱重疊')
            return
        if colorname=="":
            QtWidgets.QMessageBox.information(self, '警告', '顏色名稱不能為空白')
            return
        self.data["colornames"][index]=colorname
        savejson(datajson_path,self.data)
        self.loaddancer()
        self.loadcolor()
        self.loadcolors()
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#showcolor
    def colorpreview(self):
        index=self.ui.colors.currentIndex()
        self.ui.colorpreview.setStyleSheet("QWidget { background-color: %s }" 
                                   % self.data["color"][index])
#快進
    def forward(self):
        self.html.page().runJavaScript(f"setTime({self.time+0.1});")
    def backward(self):
        self.html.page().runJavaScript(f"setTime({self.time-0.1});") 
    def zoomin(self):
        self.html.page().runJavaScript(f"increaseSliderValue();") 
    def zoomout(self):
        self.html.page().runJavaScript(f"decreaseSliderValue();")
    def scrollleft(self):
        self.html.page().runJavaScript(f"scrollWaveSurferLeft()")
    def scrollright(self):
        self.html.page().runJavaScript(f"scorllWaveSurferRight()")
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())