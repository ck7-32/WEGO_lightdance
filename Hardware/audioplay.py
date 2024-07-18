from pygame import mixer  # Load the popular external library
import os
path=os.path.abspath(__file__)
pathpf = path[0:path.rfind('\\')]
import subprocess

audio_path=r"\0701audio.mp3"


def play():
    music_file_path = pathpf + audio_path
    mixer.init()
    mixer.music.load(music_file_path)
    mixer.music.play()
    print("play")

def get_windows_ssid():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "SSID" in line:
            ssid = line.split(':')[1].strip()
            return ssid
    return None

while True:
    if not get_windows_ssid()=="LightDanceServer":
        break
play()
input()