import os
import tkinter as tk
import whisper

class GUI:
    def __init__(self, root, audio_recorder, transcriber):
        self.root = root
        self.audio_recorder = audio_recorder
        self.transcriber = transcriber
        self.translated_text = ""
        self.record_button = None
        self.stop_button = None
        self.text_box = None
        self.play_audio_button = None

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="EchoTranslate",
            font=("Roboto", 32),
            fg="purple"
        )
        self.title_label.pack(pady=20)

        self.record_button = tk.Button(
            self.root,
            text="Gravar",
            command=self.start_recording,
            font=("Arial", 16),
            bg="#006400",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#008000",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root,
            text="Parar gravação",
            state=tk.DISABLED,
            command=self.stop_recording,
            font=("Arial", 16),
            bg="#006400",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#008000",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.stop_button.pack(pady=10)

        self.play_audio_button = tk.Button(
            self.root,
            text="Tocar Áudio",
            state=tk.DISABLED,
            command=self.play_audio,
            font=("Arial", 16),
            bg="#006400",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#008000",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.play_audio_button.pack_forget()

        self.text_box = tk.Text(self.root, height=10, width=50)
        self.text_box.pack_forget()

    def start_recording(self):
        # Hide play button and invert buttons state
        self.play_audio_button.pack_forget()
        self.text_box.pack_forget()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.ACTIVE)
        self.translated_text = ""
        # Start recording
        self.audio_recorder.start_recording()

    def stop_recording(self):
        self.audio_recorder.stop_recording()

        # Save recording
        filename = "recording.wav"
        self.audio_recorder.save_recording(filename)
        print(f"Arquivo de áudio: {filename}")
        # Enable and disabled buttons
        self.stop_button.config(state=tk.DISABLED)
        self.record_button.config(state=tk.ACTIVE)
        self.play_audio_button.pack(pady=10)
        self.play_audio_button.config(state=tk.ACTIVE)
        self.show_text()

    def transcribe_text(self):
        if self.translated_text != "":
            return self.translated_text
        text = self.transcriber.audio_to_text("recording.wav", "pt")
        translated = self.transcriber.translate(text, "en")
        self.translated_text = translated
        return translated

    def show_text(self):
        text = self.transcribe_text()
        # put text in text box
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text)
        self.text_box.pack(pady=10)
        self.text_box.config(state=tk.DISABLED)

    def play_audio(self):
        text = self.transcribe_text()
        filename = self.transcriber.text_to_audio(text, "translated_recording.mp3", 'en')
        # Start the audio file
        os.system("mpg123 " + filename)

    def run(self):
        self.root.title("EchoTranslate")
        self.root.geometry("400x600")
        self.root.resizable(True, True)
        self.create_widgets()
        self.root.mainloop()

