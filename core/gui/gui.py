import os
import tkinter as tk
import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator

class GUI:
    def __init__(self, root, audio_recorder):
        self.root = root
        self.audio_recorder = audio_recorder
        self.record_button = None
        self.stop_button = None
        self.show_text_button = None
        self.play_audio_button = None

    def create_widgets(self):
        self.record_button = tk.Button(
            self.root,
            text="Gravar",
            command=self.start_recording,
            font=("Arial", 16),
            bg="#008000",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#006400",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root,
            text="Parar",
            state=tk.DISABLED,
            command=self.stop_recording,
            font=("Arial", 16),
            bg="#008000",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#006400",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.stop_button.pack(pady=10)

        self.show_text_button = tk.Button(
            self.root,
            text="Mostrar Texto",
            state=tk.DISABLED,
            command=self.transcribe_text,
            font=("Arial", 16),
            bg="#008000",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#006400",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.show_text_button.pack(pady=10)

        self.play_audio_button = tk.Button(
            self.root,
            text="Tocar Áudio",
            state=tk.DISABLED,
            command=self.play_audio,
            font=("Arial", 16),
            bg="#008000",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#006400",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.play_audio_button.pack(pady=10)

    def start_recording(self):
        self.audio_recorder.start_recording()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.audio_recorder.stop_recording()
        self.stop_button.config(state=tk.DISABLED)
        self.show_text_button.config(state=tk.NORMAL)
        self.play_audio_button.config(state=tk.NORMAL)
        filename = "recording.wav"
        self.audio_recorder.save_recording(filename)
        print(f"Arquivo de áudio: {filename}")

    def transcribe_text(self):
        # Configura o modelo de linguagem para modelo médio e lingua inglesa
        model = whisper.load_model("tiny")
        # Transcreve o áudio para texto
        result = model.transcribe("recording.wav", fp16=False, language="pt")
        translated = GoogleTranslator(
            source='auto', target='en'
        ).translate(result["text"])
        print(translated)
        return translated

    def play_audio(self):
        text = self.transcribe_text()
        language = 'en'
        myobj = gTTS(text=text, lang=language, slow=True)
        myobj.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")

    def run(self):
        self.root.title("EchoTranslate")
        self.root.geometry("400x300")
        self.create_widgets()
        self.root.mainloop()

