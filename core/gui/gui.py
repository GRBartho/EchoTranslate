import tkinter as tk

class GUI:
    def __init__(self, root, audio_recorder):
        self.root = root
        self.audio_recorder = audio_recorder
        self.record_button = None
        self.stop_button = None
        self.download_button = None

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

        self.download_button = tk.Button(
            self.root,
            text="Baixar Áudio",
            state=tk.DISABLED,
            command=self.download_recording,
            font=("Arial", 16),
            bg="#008000",
            fg="#ffffff",
            relief=tk.RAISED,
            activebackground="#006400",
            activeforeground="#ffffff",
            padx=20,
            pady=10
        )
        self.download_button.pack(pady=10)

    def start_recording(self):
        self.audio_recorder.start_recording()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.audio_recorder.stop_recording()
        self.stop_button.config(state=tk.DISABLED)
        self.download_button.config(state=tk.NORMAL)

    def download_recording(self):
        filename = "recording.wav"
        self.audio_recorder.save_recording(filename)
        print(f"Arquivo de áudio: {filename}")

    def run(self):
        self.root.title("EchoTranslate")
        self.root.geometry("400x300")
        self.create_widgets()
        self.root.mainloop()

