from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel,QtGui
from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QShortcut,QStandardItemModel, QStandardItem,QColor , QPalette
from PyQt6.QtCore import Qt,QTimer
from UI.UI import Ui_MainWindow
import sys
import os
import json
import socket
import struct
import math

settingjson_path="data\setting.json"
datajson_path="data\data.json"
presetsjson_path="data\presets.json"
pos_path="data\pos.json"
index_html_path="stage/index.html"
# 設定廣播地址和埠
broadcast_address = '255.255.255.255'
broadcast_port = 12345

# 創建 UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def UDP(nowframe):
    message = struct.pack('>i', nowframe)
    sock.sendto(message, (broadcast_address, broadcast_port))
    print(f"UDP:{nowframe}幀")

def loadjson(path):
    with open(path, 'r', encoding='utf-8') as file:
        out = json.load(file)
    return out

def savejson(path,data):
    with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

#用二分搜尋法取得當前是第幾幀，輸入:(時間點陣列,時間點)
def get_time_index(time_segments, current_time):
    left = 0
    right = len(time_segments) - 1
    while left <= right:
        mid = (left + right) // 2
        segment = time_segments[mid]

        if current_time >= segment:
            left = mid + 1
        else:
            right = mid - 1

    return right

#設定顏色編輯區會用到的不同顏色的combobox連結到的物件
class ColorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 使用模型中的背景顏色
        color = index.data(Qt.ItemDataRole.BackgroundRole)
        if color:
            painter.fillRect(option.rect, color)

#處理來自前端的訊號
class CallHandler(QtCore.QObject):
    @QtCore.pyqtSlot(float)
    def receiveTime(self, time):
        MainWindow_controller.receivetime(window,time)
    @QtCore.pyqtSlot(str, float)
    def updateframe(self, id, newtime):
        MainWindow_controller.updateframe(window,id, newtime)
    @QtCore.pyqtSlot(str, float )
    def updatepostime(self, id, newtime):
        MainWindow_controller.updatepostime(window,id, newtime)
    @QtCore.pyqtSlot(int , float,float)
    def updatepos(self,dancerid,x,y):
        MainWindow_controller.updatepos(window, dancerid,x,y)
    @QtCore.pyqtSlot(str)
    def debug(self, context):
       print(context)
    @QtCore.pyqtSlot(int)
    def selectdancer(self,dancerN):
        MainWindow_controller.selectdancer(window,dancerN)


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
        html_file_path = os.path.join(current_dir, index_html_path)
        # 打印路徑以檢查是否正確
        print(f"HTML file path: {html_file_path}")
        #載入setting.json
        
        self.setting =loadjson(settingjson_path)
        self.data=loadjson(datajson_path)
        self.Pos=loadjson(pos_path)
        self.presets=loadjson(presetsjson_path)       
        self.html.setUrl(QtCore.QUrl("http://127.0.0.1:5500/stage/index.html"))

        #變數宣告
        self.time=0 #編輯器的游標時間
        self.dancerN=0 #現在所選擇的舞者是哪一個
        self.nowframe=0 #現在跑到第幾幀(顏色)
        self.nowPos=0 #現在跑到第幾幀(位置)
        self.partcolors=[self.ui.color0,self.ui.color1,self.ui.color2,self.ui.color3,self.ui.color4,self.ui.color5,self.ui.color6,self.ui.color7,self.ui.color8,self.ui.color9,self.ui.color10,self.ui.color11,self.ui.color12,self.ui.color13,self.ui.color14,self.ui.color15,self.ui.color16,self.ui.color17]
        self.partlable=[self.ui.part0,self.ui.part1,self.ui.part2,self.ui.part3,self.ui.part4,self.ui.part5,self.ui.part6,self.ui.part7,self.ui.part8,self.ui.part9,self.ui.part10,self.ui.part11,self.ui.part12,self.ui.part13,self.ui.part14,self.ui.part15,self.ui.part16,self.ui.part17]
        self.loaddancer()
        self.partnum=0 #現在所選的舞者的部位數量
        self.colormodel=QStandardItemModel()
    

        #按鈕功能綁定 初始化()
        self.ui.nowframe.setText(f"{self.nowframe}")
        self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
        self.ui.Dancers.addItems(self.setting["dancersname"])
        self.ui.Dancers.currentIndexChanged.connect(self.dancerselected)
        self.ui.colors.currentIndexChanged.connect(self.colorpreview)
        #設定全局快捷鍵
        self.setup_shortcuts()
        #設定介面按鍵
        self.setup_btn()

        self.colorupdate()
        self.dancerselected()
        self.loaddancer()
        self.reloadpresets()
        
#介面按鍵綁定
    def setup_btn(self):
        events = {
        self.ui.settimebtn: self.settime,
        self.ui.save: self.colorchanged,
        self.ui.savepreset: self.save_as_preset,
        self.ui.loadpreset: self.loadpreset,
        self.ui.delpreset: self.delpreset,
        self.ui.set_frame_start_bynowtime: self.set_frame_start_bynowtime,
        self.ui.set_frame_end_bynowtime: self.set_frame_end_bynowtime,
        self.ui.newframe: self.addnewframe,
        self.ui.delframe: self.delframe,
        self.ui.delcolor: self.delcolor,
        self.ui.loadframestarttime: self.setframestarttime,
        self.ui.addcolor: self.addnewcolor,
        self.ui.editcolor: self.editcolor,
        self.ui.renamecolor: self.editcolorname,
        self.ui.showcolor: self.colorpreview,
        self.ui.UDP: self.UDP_now,
        self.ui.debug:self.debug_btn,
        self.ui.Begining:self.jump_to_begining
        }
        # 使用迴圈批量綁定信號與槽
        for control, event_handler in events.items():
            control.clicked.connect(event_handler)
    
#快捷鍵綁定
    def setup_shortcuts(self):
        # 將快捷鍵和處理函數關聯在一起
        shortcuts = {
            '1': self.colorchanged,
            '2': self.set_frame_start_bynowtime,
            '3': self.set_frame_end_bynowtime,
            'G': lambda: self.html.page().runJavaScript("wavesurfer.playPause()"),
            'A': self.addnewframe,
            'D': self.delframe,
            'P': self.forward,
            'O': self.backward,
            '9': self.zoomin,
            '8': self.zoomout,
            '-': self.scrollleft,
            '=': self.scrollright,
            "R": self.UDP_now,
            '5': self.jump_to_begining,
            'Z': self.newpos,
            'C': self.delpos,
            "L": self.loadpreset
        }
        # 批量綁定快捷鍵
        for key, action in shortcuts.items():
            shortcut = QShortcut(QtGui.QKeySequence(key), self)
            shortcut.activated.connect(action)
#廣播
    def UDP_now(self):
        UDP(self.nowframe)
#DEBUG模式按鈕    
    def debug_btn(self):
        # 如果 DEBUG 已經是開啟狀態，則關閉它
        if hasattr(self, 'debug_active') and self.debug_active:
            # 停止定時器
            self.timer.stop()
            self.ui.debug.setText("DEBUG ON")  # 更新按鈕文字
            self.debug_active = False
        else:
            # 啟動 DEBUG 模式
            self.ui.debug.setText("DEBUG OFF")  # 更新按鈕文字
            self.debug_active = True
            
            # 設定定時器，每 10 秒切換一次幀
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.debug)  # 連結每 10 秒執行的函數
            self.timer.start(500)  # 設置每 10 秒觸發一次
#debug模式-閃爍全暗(第一幀)全亮(最後一幀)
    def debug(self):
          # 根據當前幀使用 self.settime 進行跳轉
        if self.nowframe == 0:
            # 跳轉到最後一幀
            last_frame_time = self.data["frametimes"][-1] / 1000  # 最後一幀的時間
            self.html.page().runJavaScript(f"setTime({last_frame_time});")
        else:
            # 跳轉到第 0 幀
            first_frame_time = self.data["frametimes"][0] / 1000  # 第 0 幀的時間
            self.html.page().runJavaScript(f"setTime({first_frame_time});")

#刷新正確幀數
    def updateframe(self,id,newtime):
        print(f"幀數{id}被更新為{newtime}")
        del self.data["frametimes"][int(id)]
        self.data["frametimes"].append(math.floor(newtime*1000))
        self.data["frametimes"].sort()
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")

#處裡移動位置flag
    def updatepostime(self,id,time):
        print(f"位置幀數{id}被更新為{time}")
        del self.Pos["postimes"][int(id)]
        self.Pos["postimes"].append(time)
        self.Pos["postimes"].sort()
        savejson(pos_path,self.Pos)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
# 處理位置更新
    def updatepos(self,dancerid,x,y):
        print(f"位置幀數{self.nowPos}的舞者{dancerid}被移動至({x},{y})")
        self.Pos["pos"][self.nowPos][dancerid]=[int(x),int(y)]
        savejson(pos_path,self.Pos)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
# 新增位置關鍵幀    
    def newpos(self):
        if self.Pos["postimes"][self.nowPos]==self.time:
             QtWidgets.QMessageBox.information(self, '警告', '與當前幀重疊')
             return
        
        self.Pos["pos"].insert(self.nowPos+1,self.Pos["pos"][self.nowPos])
        self.Pos["postimes"].insert(self.nowPos+1,self.time)
        savejson(pos_path,self.Pos)
        self.nowPos+=1
        self.ui.nowpos.setText(f"{self.nowPos}")
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
        self.Pos=loadjson(pos_path)
# 刪除位置關鍵幀  
    def delpos(self):
        if self.nowPos==0:
            QtWidgets.QMessageBox.information(self, '警告', '不能刪除第一幀')
            return
        
        del self.Pos["pos"][self.nowPos]
        del self.Pos["postimes"][self.nowPos]
        self.nowPos-=1
        self.ui.nowpos.setText(f"{self.nowPos}")
        savejson(pos_path,self.Pos)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")



 
#收到時間碼
    def receivetime(self,time):
        if self.time==time:
            return
        self.time=time
        self.ui.nowtime.setText(f"{time}")
        self.ui.settime.setText(f"{time}")
        frame=get_time_index(self.data["frametimes"],self.time*1000)
        posframe=get_time_index(self.Pos["postimes"],self.time)
        if self.nowPos!=posframe:
            self.nowPos=posframe
            self.ui.nowpos.setText(f"{self.nowPos}")
        if self.nowframe==frame:
            return
        self.nowframe=frame
        UDP(frame)
        self.ui.nowframe.setText(f"{self.nowframe}")
        self.ui.nowframetime.setText(str((self.data["frametimes"][self.nowframe])/1000))
        self.loaddancer()
#將舞者載入
    def loaddancer(self):
        self.setcomboboxcolor()
        self.ui.dancernow.setText(self.setting["dancersname"][self.dancerN])
        self.partnum=len(self.setting["dancers"][self.setting["dancersname"][self.dancerN]]["parts"])
        for i in range(self.partnum):
            self.partlable[i].show()
            self.partcolors[i].show()
            self.partlable[i].setText(self.setting["dancers"][self.setting["dancersname"][self.dancerN]]["parts"][i])
        for i in range(18-self.partnum):
            self.partlable[17-i].hide()
            self.partcolors[17-i].hide()
        self.loadcolor()
    

#選擇舞者選單被按下
    def dancerselected(self):
        self.dancerN=self.ui.Dancers.currentIndex()
        self.html.page().runJavaScript(f"setArrow({self.dancerN});")
        print(f"設置箭頭為{self.dancerN}")
        self.loaddancer()
#透過前端點擊收到切換舞者    
    def selectdancer(self,dancerN):
        self.ui.Dancers.setCurrentIndex(dancerN)
        self.dancerN=dancerN
        

#設定html視窗內撥放進度的時間
    def settime(self):
        time=self.ui.settime.text()
        print(time)
        self.html.page().runJavaScript(f"setTime({time});")
#將時間調整至該幀的起始時間   
    def setframestarttime(self):
        time=self.data["frametimes"][self.nowframe]/1000
        print(time)
        self.html.page().runJavaScript(f"setTime({time});")
#儲存setting.json
    def savesetting(self):
        savejson(settingjson_path,self.setting)
        
#更新選項顏色底色
    def setcomboboxcolor(self):
        self.colormodel=QStandardItemModel()
        colors=self.data["color"]
        names=self.data["colornames"]
        for i in range(len(colors)):
            item = QStandardItem()
            # 設置顯示的文字為顏色名稱
            item.setText(names[i])  
             # 設置每個項目的背景顏色
            item.setBackground(QColor(colors[i])) 
            # 添加到模型
            self.colormodel.appendRow(item)
#載入光效

#設定該顏色combobox的內容
    def set_combobox_color(self, part_index, dancer_index, frame_index):#(self,第幾個部位,第幾個舞者,第幾幀)
        combo_box = self.partcolors[part_index]
        
        # 設置顏色模型和自定義的 ColorDelegate
        combo_box.setModel(self.colormodel)
        combo_box.setItemDelegate(ColorDelegate())
        
        # 設置當前幀的顏色索引
        combo_box.setCurrentIndex(self.data["frames"][dancer_index][frame_index][part_index])
        
        # 更新 QComboBox 的背景顏色
        index = combo_box.currentIndex()
        selected_color = self.data["color"][index]
        palette = combo_box.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(selected_color))  
        combo_box.setPalette(palette)

        # 當索引變更時，更新顏色背景
        combo_box.currentIndexChanged.connect(self.update_combobox_background)

#將資料載入到下方顏色編輯區
    def loadcolor(self):
        for i in range(self.partnum):
            self.set_combobox_color(i, self.dancerN, self.nowframe)

#下方顏色編輯區變更後 更新combobox背景
    def update_combobox_background(self, index):
        # 根據當前索引設置 combo_box 顯示框的背景顏色
        selected_color = self.data["color"][index]
              # 使用 self.sender() 獲取是哪個 QComboBox 觸發了這個事件
        combo_box = self.sender()

        # 找出觸發事件的 QComboBox 在 self.partcolors 中的索引位置
        combo_index = self.partcolors.index(combo_box)
        # 使用 palette 設置編輯區域的背景顏色
        palette = self.partcolors[combo_index].palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(selected_color))  # 設置 QComboBox 顯示框的背景顏色
        self.partcolors[combo_index].setPalette(palette)    

#下方編輯區顏色資料送出變更
    def colorchanged(self):
        for i in range(len(self.setting["dancers"][self.setting["dancersname"][self.dancerN]]["parts"])):
            self.data["frames"][self.dancerN][self.nowframe][i]=self.partcolors[i].currentIndex()
        print(f"第{self.nowframe}幀已改變")
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")

#將當前舞者的顏色儲存為preset(預設檔)
    def save_as_preset(self):
        name=self.ui.presetname.text()
        print("1")
        if name =="":
            QtWidgets.QMessageBox.information(self, '警告', '輸入框不能為空')
            return
        elif name in self.presets["presetnames"]:
            QtWidgets.QMessageBox.information(self, '警告', '輸入框不能為空')
            return
        preset=[]
        for i in range(self.partnum):
            preset.append(self.partcolors[i].currentIndex())
        self.presets["presets"].append(preset)
        self.presets["presetnames"].append(name)
        savejson(presetsjson_path,self.presets)
        self.reloadpresets()


#將選中的preset載入當前的舞者
    def loadpreset(self):
        index=self.ui.presets.currentIndex()
        for i in range(len(self.setting["dancers"][self.setting["dancersname"][self.dancerN]]["parts"])):
            self.partcolors[i].setCurrentIndex(self.presets["presets"][index][i])
        self.colorchanged()

#刪除 preset
    def delpreset(self):
        index=self.ui.presets.currentIndex()
        del self.presets["presets"][index]
        del self.presets["presetnames"][index]
        savejson(presetsjson_path,self.presets)
        self.reloadpresets()

#r刷新 presets 的 combobox
    def reloadpresets(self):
        self.ui.presets.clear()
        self.ui.presets.addItems(self.presets["presetnames"])

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
        self.data["frametimes"][self.nowframe]=math.floor(time)
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
        self.data["frametimes"][self.nowframe+1]=math.floor(time)
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")

#新增關鍵幀
    def addnewframe(self):
        if self.data["frametimes"][self.nowframe]==self.time*1000:
             QtWidgets.QMessageBox.information(self, '警告', '與當前幀重疊')
             return
        for i in range(len(self.data["frames"])):
            self.data["frames"][i].insert(self.nowframe+1,self.data["frames"][i][self.nowframe])
        self.data["frametimes"].insert(self.nowframe+1,math.floor(self.time*1000))
        savejson(datajson_path,self.data)
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
        self.nowframe-=1
        self.ui.nowframe.setText(f"{self.nowframe}")
        savejson(datajson_path,self.data)
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")

#右上角顏色區

#載入 顏色到上方colors combobox
    def colorupdate(self):
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
        self.setcomboboxcolor()
        self.loadcolor()
        self.loaddancer()
        self.colorupdate()
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
            self.setcomboboxcolor()
            self.loaddancer()
            self.loadcolor()
            self.colorupdate()
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
            self.setcomboboxcolor()
            self.loaddancer()
            self.loadcolor()
            self.colorupdate()
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
        self.colorupdate()
        self.html.page().runJavaScript(f"reloadDataAndRedraw();")
#預覽顏色
    def colorpreview(self):
        index=self.ui.colors.currentIndex()
        self.ui.colorpreview.setStyleSheet("QWidget { background-color: %s }" 
                                   % self.data["color"][index])

#快進快退
    def forward(self):
        self.html.page().runJavaScript(f"setTime({self.time+0.1});")
    def backward(self):
        self.html.page().runJavaScript(f"setTime({self.time-0.1});") 
#放大縮小時間軸
    def zoomin(self):
        self.html.page().runJavaScript(f"increaseSliderValue();") 
    def zoomout(self):
        self.html.page().runJavaScript(f"decreaseSliderValue();")
#滾動時間軸
    def scrollleft(self):
        self.html.page().runJavaScript(f"scrollWaveSurferLeft()")
    def scrollright(self):
        self.html.page().runJavaScript(f"scrollWaveSurferRight()")

#跳至開頭
    def jump_to_begining(self):
        self.html.page().runJavaScript(f"setTime({0});") 


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())

#
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#              佛祖保佑          永無BUG