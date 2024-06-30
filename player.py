from pygame import mixer
import os
import tkinter as tk
from tkinter import messagebox

# Get the current file path and determine the parent directory
path = os.path.abspath(__file__)
pathpf = os.path.dirname(path)

# Audio file path

audio_path = r"\0701audio.mp3"
music_file_path = pathpf + audio_path
mixer.init()
mixer.music.load(music_file_path)

def play():
    mixer.music.play()


root = tk.Tk()
root.title("Music Player")
root.mainloop()