import tkinter as tk
import time
# import requests
import webbrowser
# import pyautogui
import os
from pygame import mixer  # Load the popular external library
import os

# from ping3 import ping
path=os.path.abspath(__file__)
print(path)

pathpf = path[0:path.rfind('\\')]
path = pathpf + "\\index_new.html"
print(path)

pings=["","","","","",""]
def getping(ip_vars):

    

    print("Connected IPs:", ips)
    for ip in range(len(ips)):
        if ip=="":
            continue
        pings[ip]=ping(ips[ip])
    print(pings)
    
ips=["192.168.50.12"]

# 建立主視窗
root = tk.Tk()
root.title("音樂播放器")

# 設定主視窗大小
root.geometry("400x250")

# 建立左邊按鈕，設定字型大小和按鈕大小
left_button = tk.Button(root, text="開始", command=lambda: left_button_clicked(), font=("Helvetica", 12), padx=10, pady=5)
left_button.pack(side=tk.LEFT, padx=10)



def getesp(ips):
    for ip in ips:
        if ip == "" :
            continue
        webbrowser.open(f"{ip}/start") 

# 定義左邊按鈕的點擊事件
def left_button_clicked():
    getesp(ips)
    time.sleep(0.05)
    music_file_path = pathpf + r"\2024.mp3"
    mixer.init()
    mixer.music.load(music_file_path)
    mixer.music.play()
    # os.system("pause")
    
    

    
# 啟動主迴圈
root.mainloop()