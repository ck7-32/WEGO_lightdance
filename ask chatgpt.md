editor.py:
```python
from PyQt6 import QtWidgets,QtCore, QtWebEngineWidgets, QtWebChannel
from UI import Ui_MainWindow
import sys
import os
import json
import time as la


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
        self.html.setUrl(QtCore.QUrl("http://127.0.0.1:5500/newtype/index.html"))

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
        self.reloadpresets()
        self.ui.set_frame_start_bynowtime.clicked.connect(self.set_frame_start_bynowtime)
        self.ui.set_frame_end_bynowtime.clicked.connect(self.set_frame_end_bynowtime)
#刷新視窗
        
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
#儲存setting.json
    def savesetting(self):
        savejson(settingjson_path,self.setting)
        
#快捷鍵
    def keyPressEvent(self, event):
        keycode = event.key()             
        if keycode == 49: 
            self.colorchanged()
            print("colorchanged")
        if keycode == 50:
            self.set_frame_start_bynowtime()
            print("設為開始時間")
        if keycode == 51:
            self.set_frame_end_bynowtime()
            print("設為結束時間")
        return
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
       # time=self.time
       ## la.sleep(10):
       # self.html.page().runJavaScript(f"setTime({time});")
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

        
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
```
index.html:
```html
<!DOCTYPE HTML>
<html>
<head>
    <style>
        body {
            margin: 0px;
            padding: 10px;
            background-color: #000000;
            color: #FFFFFF;
        }
        #waveform {
            width: 850px;
            height: 100px;
            background-color: #000000;
            margin: 0 auto;
        }
        #zoom-slider {
            width: 850px;
            margin: 20px auto;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/2.6.0/webcomponents-loader.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/systemjs/6.9.0/system.min.js"></script>
    <script src="qwebchannel.js"></script>

    <script>
        let regionsPlugin;

        document.addEventListener('DOMContentLoaded', function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.handler = channel.objects.handler;
                console.log('QWebChannel initialized');
            });
        });

        function getCurrentTime() {
            var currentTime = wavesurfer.getCurrentTime();
            console.log('Current Time:', currentTime);
            if (typeof handler !== 'undefined') {
                handler.receiveTime(currentTime);
            } else {
                console.error('Handler is not defined');
            }
        }

        function setTime(time) {
            const duration = wavesurfer.getDuration();
            const progress = time / duration;
            wavesurfer.seekTo(progress);
        }

        async function updateFrameTimes(regions) {
            const frametimes = regions.map(region => region.start * 1000); // 转换为毫秒
            frametimes.push(regions[regions.length - 1].end * 1000); // 添加最后一个区域的结束时间

            const data = { frametimes };

            try {
                const response = await fetch('/update-fraetimes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                console.log('Frame times updated:', result);
            } catch (error) {
                console.error('Error updating frame times:', error);
            }
        }

        function reloadRegions() {
            fetch('data.json')
                .then(response => response.json())
                .then(data => {
                    const frametimes = data.frametimes;
                    regionsPlugin.clearRegions(); // 清除现有的regions
                    for (let i = 0; i < frametimes.length - 1; i++) {
                        const startTime = frametimes[i] / 1000; // 转换为秒
                        const endTime = frametimes[i + 1] / 1000; // 转换为秒
                        regionsPlugin.addRegion({
                            start: startTime,
                            end: endTime,
                            color: i % 2 === 0 ? 'rgba(50, 0, 0, 0.5)' : 'rgba(0, 50, 0, 0.5)', // 基数偶数段不同颜色
                            resize: false, // 允许调整大小
                            drag: false // 允许拖动
                        });
                    }
                    // 添加最后一个时间点的标记
                    const lastStartTime = frametimes[frametimes.length - 1] / 1000;
                    regionsPlugin.addRegion({
                        start: lastStartTime,
                        end: lastStartTime + 0.5, // 给最后一个标记一个默认的持续时间
                        color: frametimes.length % 2 === 0 ? 'rgba(50, 0, 0, 0.5)' : 'rgba(0, 50, 0, 0.5)', // 基数偶数段不同颜色
                        resize: false, // 允许调整大小
                        drag: false // 允许拖动
                    });
                })
                .catch(error => console.error('Error loading data.json:', error));
        }

        function reloadDataAndRedraw() {
            fetchDataAndInitialize();
            reloadRegions(); // 新增这行
        }
    </script>
</head>
<body>
    <center>
        <canvas id="myCanvas" width="850" height="300" style="background-color: #000000" autoplay></canvas>
        <div id="waveform"></div>
        <input id="zoom-slider" type="range" min="1" max="200" value="100">
    </center>

    <script type="text/javascript" src="pos.js" charset="utf-8"></script>
    <script type="text/javascript" src="main.js" charset="utf-8"></script>
    <div id="audiowave"></div>
    <script type="module">
        import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js';
        import RegionsPlugin from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/regions.esm.js';

        window.wavesurfer = WaveSurfer.create({
            container: '#waveform',
            waveColor: '#FFFFFF',
            progressColor: '#8a8a8a',
            url: '成發(final).mp3',
            height: 128,
            hideScrollbar: true,
            interact: true // 允许拖动进度条
        });

        regionsPlugin = RegionsPlugin.create();
        wavesurfer.registerPlugin(regionsPlugin);

        wavesurfer.on('ready', () => {
            console.log('WaveSurfer is ready');
            // 从data.json加载时间标记
            fetch('data.json')
                .then(response => response.json())
                .then(data => {
                    const frametimes = data.frametimes;
                    for (let i = 0; i < frametimes.length - 1; i++) {
                        const startTime = frametimes[i] / 1000; // 转换为秒
                        const endTime = frametimes[i + 1] / 1000; // 转换为秒
                        regionsPlugin.addRegion({
                            start: startTime,
                            end: endTime,
                            color: i % 2 === 0 ? 'rgba(50, 0, 0, 0.5)' : 'rgba(0, 50, 0, 0.5)', // 基数偶数段不同颜色
                            resize: false, // 允许调整大小
                            drag: false // 允许拖动
                        });
                    }
                    // 添加最后一个时间点的标记
                    const lastStartTime = frametimes[frametimes.length - 1] / 1000;
                    regionsPlugin.addRegion({
                        start: lastStartTime,
                        end: lastStartTime + 0.5, // 给最后一个标记一个默认的持续时间
                        color: frametimes.length % 2 === 0 ? 'rgba(50, 0, 0, 0.5)' : 'rgba(0, 50, 0, 0.5)', // 基数偶数段不同颜色
                        resize: false, // 允许调整大小
                        drag: false // 允许拖动
                    });
                })
                .catch(error => console.error('Error loading data.json:', error));
        });

        regionsPlugin.on('region-update-end', () => {
            const regions = Object.values(wavesurfer.regions.list);
            updateFrameTimes(regions);
        });

        wavesurfer.on('seek', (progress) => {
            const duration = wavesurfer.getDuration();
            const newTime = progress * duration;
            getCurrentTime(newTime);
        });

        document.getElementById('zoom-slider').oninput = function() {
            wavesurfer.zoom(Number(this.value));
        };
    </script>
</body>
</html>
```

main.js:
```Javascript
var N_PART = 16;
var N_DANCER = 3;

document.addEventListener('DOMContentLoaded', function() {
  var audioElement = document.getElementById('myAudio');
  wavesurfer.play();
});
var DELAY = 0.0;

var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
ctx.lineWidth = 3;

var BLUE = "#00FFFF";
var ORANGE = "#FF9400";
var YELLOW = "#FFFF00";
var PURPLE = "#AA00FF";
var RED = "#FF0000";
var WHITE = "#FFFFFF";
var GREEN = "#99FF33";
var BLACK = "#000000";
var PINK = "#FFC0CB";
var COLOR=[BLACK,RED,PINK,ORANGE,GREEN,BLUE,PURPLE,WHITE]

function color(c, x) {
  var percent = (-1) * (1.0 - (x / 255.0));
  return c;
}
Pos = JSON.parse(Pos);

function fetchDataAndInitialize() {
  fetch('data.json')
    .then(response => response.json())
    .then(data => {
      alllight = data.frames;
      frametime = data.frametimes;

      startAnimation();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}
function reloadDataAndRedraw() {
  fetchDataAndInitialize();
  reloadRegions(); // 新增這行
  getCurrentTime();
}
function setTime(time) {
  const duration = wavesurfer.getDuration();
  const progress = time / duration;
  wavesurfer.seekTo(progress);
}
function startAnimation() {
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
      function(callback) {
        window.setTimeout(callback, 1000);
      };
  })();

  window.addEventListener("keydown", (e) => {
    if(e.keyCode === 32){
      if(wavesurfer.isPlaying()) wavesurfer.pause();
      else wavesurfer.play();
    }
    else if(e.keyCode === 37){
      setTime(wavesurfer.getCurrentTime() - 5);
    }
    else if(e.keyCode === 39){
      setTime(wavesurfer.getCurrentTime() + 5);
    }
    else if(e.keyCode === 190){
      setTime(wavesurfer.getCurrentTime() + 0.1);
    }
    else if(e.keyCode === 188){
      setTime(wavesurfer.getCurrentTime() - 0.1);
    }
    else if (event.key === 'k' || event.key === 'K') {
      wavesurfer.playPause();  // 切換播放/暫停
  }});

  function getPos(idx, time) {
    var bx = 0, by = 0;
    var S = Pos[idx].length;

    if(S == 0) return [0, 0];

    var lb = 0, rb = S-1;
    while(lb < rb) {
      var mb = (lb + rb + 1) >> 1;
      if(Pos[idx][mb][0] > time)
        rb = mb - 1;
      else
        lb = mb;
    }

    var t1 = Pos[idx][lb][0];
    var x1 = Pos[idx][lb][1];
    var y1 = Pos[idx][lb][2];

    if(lb == S-1) return [x1, y1];
    
    var t2 = Pos[idx][lb+1][0];
    var x2 = Pos[idx][lb+1][1];
    var y2 = Pos[idx][lb+1][2];

    bx = x1 + (x2-x1) * (time-t1) / (t2-t1);
    by = y1 + (y2-y1) * (time-t1) / (t2-t1);

    return [bx, by];
  }

  function getTimeSegmentIndex(timeSegments, currentTime) {
    let left = 0;
    let right = timeSegments.length - 1;

    while (left <= right) {
      const mid = Math.floor((left + right) / 2);
      const segment = timeSegments[mid];

      if (currentTime >= segment) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }
    return right;
  }

  function draw_time(time, frame) {
    ctx.font = "20px Monospace";
    ctx.fillStyle = "#FFFFFF";
    
    ctx.fillText(frame, 0, canvas.height - 40);
    ctx.fillText(time, 0, canvas.height - 20);
  }

  function animate(darr, canvas, ctx, startTime) {
    var time = wavesurfer.getCurrentTime() + DELAY;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for(var i=0; i<N_DANCER; i++) {
      for(var j=0; j<N_PART; j++) {
        var pos = getPos(i, time);
        darr[i].setBasePos(pos[0], pos[1]);
      }
    }

    for(var i=0; i<N_DANCER; i++)
      darr[i].draw(time);

    segment = getTimeSegmentIndex(frametime, time * 1000);
    draw_time(time, segment);

    requestAnimFrame(function() {
      animate(darr, canvas, ctx, startTime);
      getCurrentTime();
    });
  }

  function animate_test(dancer, canvas, ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(var j = 0; j < N_PART; j++) {
      dancer.setLight(j, 255);
    }
    dancer.setBasePos(canvas.width / 2, canvas.height / 2);
    dancer.draw();
  }

  function getcolor(dancer, segment, part) {
    return COLOR[alllight[dancer][segment][part]];
  }

  function Dancer(id, bx, by) {
    this.id = id;
    this.base_x = bx;
    this.base_y = by;
    this.height = 160;
    this.width = 64;
    this.light = Array(N_PART);
    for(var i=0; i<N_PART; i++)
      this.light[i] = 0;
  };

  Dancer.prototype.setBasePos = function(bx, by) {
    this.base_x = bx;
    this.base_y = by;
  }

  Dancer.prototype.draw = function(time) {
    var miltime = time * 1000;
    var segment = getTimeSegmentIndex(frametime, miltime);

    ctx.strokeStyle = "#FFFFFF";
    ctx.strokeRect(this.base_x, this.base_y, 1, 1);
    ctx.strokeRect(this.base_x + this.width, this.base_y, 1, 1);
    ctx.strokeRect(this.base_x, this.base_y + this.height, 1, 1);
    ctx.strokeRect(this.base_x + this.width, this.base_y + this.height, 1, 1);

    var head_radius = 20;
    ctx.font = "20px sans-serif";
    ctx.fillStyle = "#FF0000";
    ctx.fillText(this.id, this.base_x + this.width / 2 - 5, this.base_y + head_radius + 6);

    ctx.strokeStyle = getcolor(this.id, segment, 2);
    ctx.beginPath();
    ctx.arc(this.base_x + this.width / 2, this.base_y + head_radius, head_radius - 3, Math.PI, Math.PI * 2);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 - 1, this.base_y + 3);
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 3, this.base_y + 0.5 * head_radius + 5);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 4, this.base_y + 1);
    ctx.lineTo(this.base_x + this.width / 2 + 1, this.base_y + 3);
    ctx.stroke();

    var hand_w = 10;
    var hand_h = 25;

    ctx.strokeStyle = getcolor(this.id, segment, 5);
    ctx.strokeRect(this.base_x, this.base_y + head_radius - 10 + hand_h + 5, hand_w, hand_h * 2);
    ctx.strokeStyle = getcolor(this.id, segment, 6);
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + head_radius - 10 + hand_h + 5, hand_w, hand_h * 2);

    var hand_radius = 6;
    ctx.strokeStyle = getcolor(this.id, segment, 3);
    ctx.beginPath();
    ctx.strokeRect(this.base_x, this.base_y + 3 * head_radius + hand_h + 5, hand_w, 3);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 4);
    ctx.beginPath();
    ctx.strokeRect(this.base_x + this.width - hand_w, this.base_y + 3 * head_radius + hand_h + 5, hand_w, 3);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 0);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2, this.base_y + 2 * head_radius + 4);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 20);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2, this.base_y + 2 * head_radius + 4);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 1);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 25);
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 2 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 2 * head_radius + 30);
    ctx.stroke();

    var belt_w = 2 * head_radius - 6;
    var belt_h = 10;
    var pants_w = 12;
    var pants_h = 35;

    ctx.strokeStyle = getcolor(this.id, segment, 8);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 7 - pants_w, this.base_y + 5 * head_radius);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 7);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 5 * head_radius);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 7 + pants_w, this.base_y + 5 * head_radius);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 9);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 - head_radius + 5 + pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.stroke();

    ctx.strokeStyle = getcolor(this.id, segment, 10);
    ctx.beginPath();
    ctx.moveTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30 + pants_h);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w, this.base_y + 4 * head_radius + 30);
    ctx.lineTo(this.base_x + this.width / 2 + head_radius - 5 - pants_w / 2, this.base_y + 3 * head_radius + 25);
    ctx.stroke();
  };

  var darr = Array(N_DANCER);
  for(var i = 0; i < N_DANCER; i++)
    darr[i] = new Dancer(i, 50 + 100 * i, 59);

  setTimeout(function() {
    var startTime = (new Date()).getTime();
    animate(darr, canvas, ctx, startTime);
  }, 500);

}

fetchDataAndInitialize();
```
我會先用live server將html運行在localprot 5050上

我在python視窗點擊self.ui.set_frame_start_bynowtime跟self.ui.set_frame_end_bynowtime
之後 對於html內的快捷鍵會失效 而且html回傳給python的時間會有很大的延遲