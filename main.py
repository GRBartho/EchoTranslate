from core.audio.audio_recorder import AudioRecorder
from core.gui.gui import GUI
from core.transcribe.transcribe import Transcribe
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    audio_recorder = AudioRecorder()
    transcriber = Transcribe()
    app = GUI(root, audio_recorder, transcriber)
    app.run()
  