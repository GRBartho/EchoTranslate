import os
import tkinter as tk
from tkinter import ttk
from tkmacosx import Button
import time

class GUI:
    def __init__(self, root, audio_recorder, transcriber):
        # Logic
        self.audio_recorder = audio_recorder
        self.transcriber = transcriber
        self.translated_text = ""
        self.should_auto_play_audio = False
        # Layout
        self.root = root
        self.record_button = None
        self.stop_button = None
        self.text_box = None
        self.play_audio_button = None
        self.auto_play_audio = None
        # Language
        self.input_language = tk.StringVar(value="pt")  # Language of input
        self.output_language = tk.StringVar(value="en")  # Language of output

    def create_widgets(self):
        '''Create all widgets on their initial state'''
        self.title_label = tk.Label(
            self.root,
            text="EchoTranslate",
            font=("Roboto", 40),
            fg="#7857EC"
        )
        self.title_label.pack(pady=20)

        # Language selectors
        language_frame = tk.Frame(self.root)
        language_frame.pack()

        input_label = tk.Label(language_frame, text="Língua de entrada:")
        input_label.pack(side=tk.TOP)

        input_combobox = ttk.Combobox(language_frame, textvariable=self.input_language)
        input_combobox['values'] = ('pt', 'en', 'es', 'fr')  # Add more languages as needed
        input_combobox.pack(side=tk.TOP)

        output_label = tk.Label(language_frame, text="Língua de saída:")
        output_label.pack(side=tk.TOP)

        output_combobox = ttk.Combobox(language_frame, textvariable=self.output_language)
        output_combobox['values'] = ('en', 'pt', 'es', 'fr')  # Add more languages as needed
        output_combobox.pack(side=tk.TOP)

        self.record_button = Button(
            self.root,
            text="Gravar",
            command=self.on_click_start_recording,
            font=("Arial", 16),
            bg="#e31837",
            fg="#ffffff",
            activebackground="#e31837",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            padx=20,
            pady=10
        )
        self.record_button.pack(pady=10)

        self.stop_button = Button(
            self.root,
            text="Parar gravação",
            state=tk.DISABLED,
            command=self.on_click_stop_recording,
            font=("Arial", 16),
            activebackground="#e31837",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            padx=20,
            pady=10
        )
        self.stop_button.pack(pady=10)

        self.play_audio_button = Button(
            self.root,
            text="Ouvir áudio",
            state=tk.DISABLED,
            command=self.on_click_play_audio,
            font=("Arial", 16),
            activebackground="#e31837",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            padx=20,
            pady=10
        )
        self.play_audio_button.pack_forget()

        self.auto_play_audio = tk.Checkbutton(
            self.root,
            text="Ouvir áudio automaticamente",
            command=self.activate_auto_play,
            font=("Arial", 16),
            fg="#ffffff",
            relief=tk.RAISED,
            variable=self.should_auto_play_audio,
            activeforeground="#ffffff",
            padx=20,
            pady=10,
        )
        self.auto_play_audio.pack(pady=10)

        self.text_box = tk.Text(self.root, height=10, width=50)
        self.text_box.pack_forget()

    def on_click_start_recording(self):
        '''Handle click on record button'''
        # Hide play and text and invert buttons state
        self.text_box.pack_forget()
        self.play_audio_button.pack_forget()
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.ACTIVE)
        # Start recording
        self.start_recording()

    def on_click_stop_recording(self):
        '''Handle click on stop recording button'''
        self.stop_button.config(state=tk.DISABLED)
        # Stop recording
        self.stop_recording()
        # Show results
        time.sleep(1)
        self.record_button.config(state=tk.ACTIVE)
        self.play_audio_button.pack(pady=10)
        self.show_text()
        if self.should_auto_play_audio:
            # Play audio if auto play is active
            self.play_audio()
        else:
            self.play_audio_button.config(state=tk.ACTIVE)

    def on_click_play_audio(self):
        '''Handle click on play audio button'''
        self.play_audio_button.config(state=tk.DISABLED)
        self.play_audio()
        time.sleep(1)
        self.play_audio_button.config(state=tk.ACTIVE)

    def start_recording(self):
        '''Starts recording from audio_recorder'''
        self.translated_text = ""
        self.audio_recorder.start_recording()

    def stop_recording(self):
        '''Stops recording from audio_recorder and saves it to a file'''
        self.audio_recorder.stop_recording()
        # Save recording
        filename = "recording.wav"
        self.audio_recorder.save_recording(filename)
        print(f"Arquivo de áudio: {filename}")

    def show_text(self):
        text = self.transcribe_text()
        # put text in text box
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text)
        self.text_box.pack(pady=10)
        self.text_box.config(state=tk.DISABLED)

    def transcribe_text(self):
        '''Transcribes audio to text and translates it to selected language'''
        if self.translated_text != "":
            return self.translated_text
        text = self.transcriber.audio_to_text("recording.wav", self.input_language.get())
        translated = self.transcriber.translate(text, self.output_language.get())
        self.translated_text = translated
        return translated

    def play_audio(self):
        '''Plays audio from transcribed text'''
        text = self.transcribe_text()
        filename = self.transcriber.text_to_audio(text, "translated_recording.mp3", self.output_language.get())
        # Start the audio file
        os.system("mpg123 " + filename)

    def activate_auto_play(self):
        '''Activates auto play'''
        self.should_auto_play_audio = not self.should_auto_play_audio

    def run(self):
        '''Starts the GUI'''
        self.root.title("EchoTranslate")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.create_widgets()
        self.root.mainloop()
