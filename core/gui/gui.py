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
        self.switch_language_button = None
        # Language
        self.input_language = tk.StringVar(value="pt")  # Language of input
        self.output_language = tk.StringVar(value="en")  # Language of output

    def _get_widgets(self):
        combostyle = ttk.Style()

        combostyle.theme_create('combostyle', parent='alt',
            settings = {'TCombobox': {'configure': {
                'fieldbackground': '#76767A',
                'selectbackground': '#76767A',
                'background': '#7857EC',
        }}}
        )
        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        combostyle.theme_use('combostyle') 

        self.title_label = tk.Label(
            self.root,
            text="EchoTranslate",
            font=("Roboto", 40),
            fg="#7857EC"
        )
        # Language selectors
        language_frame = tk.Frame(self.root)
        self.language_frame = language_frame
        self.input_label = tk.Label(language_frame, text="Língua de Entrada:")
        self.input_combobox = ttk.Combobox(
            language_frame, 
            textvariable=self.input_language,
            width=15,
            state=tk.FLAT,
        )
        self.input_combobox['values'] = ('pt', 'en', 'es', 'fr','ja', 'ru')  # Add more languages as needed
        self.output_label = tk.Label(language_frame, text="Língua de Saída:")
        self.output_combobox = ttk.Combobox(
            language_frame,
            textvariable=self.output_language,
            width=15,
            state=tk.FLAT,
        )
        self.output_combobox['values'] = ('pt', 'en', 'es', 'fr','ja', 'ru')  # Add more languages as needed
        # Buttons
        photo = tk.PhotoImage(file = r"assets/change_icon.png")
        photoimage = photo.subsample(70, 70)
        self.switch_language_button = Button(
            self.root,
            image=photoimage,
            command=self.on_click_switch_language,
            font=("Arial", 16),
            width=30,
            height=30,
            bg="#76767A",
            fg="#ffffff",
            activebackground="#76767A",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.record_button = Button(
            self.root,
            text="Iniciar gravação",
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
        # Others
        self.text_box = tk.Text(self.root, height=10, width=50)
        self.auto_play_audio = tk.Checkbutton(
            self.root,
            text="Ouvir áudio automaticamente",
            command=self.activate_auto_play,
            font=("Arial", 16),
            fg="#ffffff",
            relief=tk.RAISED,
            variable=self.should_auto_play_audio,
            activeforeground="#ffffff",
            selectcolor="#7857EC",
            padx=20,
            pady=10,
        )

    def create_layout_widgets(self):
        '''Create all widgets on their initial grid state'''
        self.root = tk.Frame(self.root)
        self.root.grid()
        self._get_widgets()
       
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.language_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.input_label.grid(row=2, column=0, pady=0)
        self.input_combobox.grid(row=3, column=0, padx=(30, 30))
        self.output_label.grid(row=2, column=2, pady=0)
        self.output_combobox.grid(row=3, column=2, padx=(30, 30))
        self.switch_language_button.grid(row=1, column=1, padx=20, pady=(20, 0))

        self.record_button.grid(row=5, column=0, columnspan=3, pady=12)
        self.stop_button.grid(row=6, column=0, columnspan=3, pady=(12, 24))
        
        self.auto_play_audio.grid(row=7, column=0, columnspan=3, pady=0)

        self.play_audio_button.grid(row=8, column=0, columnspan=3, pady=(24, 12))
        self.play_audio_button.grid_remove()

        self.text_box.grid(row=9, column=0, columnspan=3, padx=20)
        self.text_box.grid_remove()

    def on_click_switch_language(self):
        '''Handle click on switch language button'''
        inputLanguage = self.input_language.get()
        self.input_language.set(self.output_language.get())
        self.output_language.set(inputLanguage)

    def on_click_start_recording(self):
        '''Handle click on record button'''
        # Hide play and text and invert buttons state
        self.play_audio_button.grid_remove()
        self.text_box.grid_remove()
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
        self.play_audio_button.grid()
        self.show_text()
        if self.should_auto_play_audio:
            # Play audio if auto play is active
            self.play_audio()
            self.play_audio_button.config(state=tk.ACTIVE)
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
        self.text_box.grid()
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
        self.root.geometry("426x620")
        self.root.resizable(False, False)
        self.create_layout_widgets()
        self.root.mainloop()
