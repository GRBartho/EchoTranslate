import tkinter as tk
import speech_recognition as sr
from threading import Thread
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class EchoTranslate:
    def __init__(self, display_text: tk.Text, display_translated: tk.Text, app_instance: object) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.app_instance = app_instance
        self.display_text = display_text
        self.display_translated = display_translated

        perform = Thread(target=self.perform)
        perform.start()

    def perform(self) -> None:
        with self.microphone as source:
            while self.app_instance.is_recording:
                audio_data = self._listen(source)
                translate_thread = Thread(target = self._translate,
                                          args = (audio_data,))
                translate_thread.start()

    def _listen(self, source: sr.Microphone) -> sr.AudioData:
        self.recognizer.adjust_for_ambient_noise(source)

        if self.app_instance.play_back_type == "Echo":
            audio_data = self.recognizer.record(source, duration = 5)

            return audio_data
        
        chunks = []
        while self.app_instance.is_recording:
            chunk = self.recognizer.record(source, duration = 1)
            chunks.append(chunk)
        
        frame_data = b"".join(chunk.frame_data for chunk in chunks)
        sample_rate = chunks[0].sample_rate if chunks else 16000
        sample_width = chunks[0].sample_width if chunks else 2

        audio_data = sr.AudioData(sample_rate=sample_rate, sample_width=sample_width, frame_data=frame_data)

        return audio_data


    def _playAudio(self, text: str) -> None:
        tts = gTTS(text = text, lang = "en", slow = True)

        tts.save("Result.mp3")

        audio_file = AudioSegment.from_file("Result.mp3")
        play(audio_file)

    def _translate(self, audio_data) -> True:
        try:
            text = self.recognizer.recognize_google(audio_data, language = "pt-BR")
            translated = GoogleTranslator(source = "auto", target = "en").translate(text)

            self.display_text.insert(tk.END, text)
            self.display_translated.insert(tk.END, translated)
            
            if self.app_instance.play_back:
                self._playAudio(translated)

            return True

        except sr.UnknownValueError:
            print("Unable to recognize speech")

        except sr.RequestError as e:
            print("Error: {0}".format(e))
