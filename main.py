from core.audio.audio_recorder import AudioRecorder
from core.gui.gui import GUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    audio_recorder = AudioRecorder()
    app = GUI(root, audio_recorder)
    app.run()
  