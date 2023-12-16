import tkinter as tk
import time
import requests
import webbrowser
import pyautogui
from ping3 import ping
path="index_new.html"
pings=[]
def getping(ip_vars):


    # 獲取輸入框的內容 
    ips = [ip_var.get() for ip_var in ip_vars]
    print("Connected IPs:", ips)
    for ip in range(len(ips)):
        if ip=="":
            continue
        pings[ip]=ping(ips[ip])
    print(pings)
    
        

# 建立主視窗
root = tk.Tk()
root.title("音樂播放器")

# 設定主視窗大小
root.geometry("400x250")

# 建立左邊按鈕，設定字型大小和按鈕大小
left_button = tk.Button(root, text="開始", command=lambda: left_button_clicked(ip_vars), font=("Helvetica", 12), padx=10, pady=5)
left_button.pack(side=tk.LEFT, padx=10)
button2=tk.Button(root,text="取得延遲",command=lambda: getping(ip_vars), font=("Helvetica", 12), padx=10, pady=5)
button2.pack(side=tk.LEFT, padx=10)
# 建立五個輸入框的變數
ip_vars = [tk.StringVar() for _ in range(5)]

for i in range(5):
    entry_label = tk.Label(root, text=f"IP {i + 1}:")
    entry_label.pack()

    entry = tk.Entry(root, textvariable=ip_vars[i])
    entry.pack()

# 定義左邊按鈕的點擊事件
def left_button_clicked(vars):
    requests.get(vars[0])
    music_file_path = "LED light dance.mp3"
    webbrowser.open(path)
    time.sleep(0.2)
    pyautogui.press('space') #按下enter鍵

# 啟動主迴圈
root.mainloop()