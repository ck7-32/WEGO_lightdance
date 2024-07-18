import tkinter as tk
from tkinter import messagebox
import os
import threading
import time
import subprocess

# Check network status function
def check_network_status():
    try:
        # Ping Google DNS (8.8.8.8)
        output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"]).decode("utf-8")
        if "1 packets transmitted, 1 packets received" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Play music function
def play_music(folder):
        os.system(f"start {"0701audio.mp3"}")

# GUI class
class WiFiMusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Music Player")

        self.music_folder = "0701audio.mp3"  # Replace with your music folder path

        # Buttons
        self.play_button = tk.Button(self.root, text="Play Music", command=self.play_music)
        self.play_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="Stop Music", command=self.stop_music)
        self.stop_button.pack(pady=10)

        # Check network status and play music in a separate thread
        self.network_thread = threading.Thread(target=self.monitor_network_and_play)
        self.network_thread.daemon = True  # Daemon thread to stop when main thread exits
        self.network_thread.start()

    def play_music(self):
        play_music(self.music_folder)

    def stop_music(self):
        # Kill any music player process (e.g., Windows Media Player)
        os.system("taskkill /F /IM wmplayer.exe")
        messagebox.showinfo("Music Stopped", "Music playback stopped.")

    def monitor_network_and_play(self):
        while True:
            if not check_network_status():
                messagebox.showwarning("WiFi Disconnected", "WiFi is disconnected. Playing music...")
                self.play_music()
            time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiMusicPlayerApp(root)
    root.mainloop()
