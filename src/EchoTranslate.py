from threading import Thread
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class EchoTranslate:
    def __init__(self, display_text, display_translated, app_instance: object) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.app_instance = app_instance
        self.display_text = display_text
        self.display_translated = display_translated

        perform = Thread(target=self.perform)
        perform.start()

    def perform(self) -> None:
        with self.microphone as source:
            while self.app_instance.is_echoing:
                audio_data = self._listen(source)
                translate_thread = Thread(target = self._translate,
                                          args = (audio_data,))
                translate_thread.start()

    def _listen(self, source: sr.Microphone) -> None:
        self.recognizer.adjust_for_ambient_noise(source)
        audio_data = self.recognizer.record(source, duration = 5)

        return audio_data

    def _playAudio(self, text: str) -> None:
        myobj = gTTS(text = text, lang = "en", slow = True)

        myobj.save("welcome.mp3")

        audio_file = AudioSegment.from_file("welcome.mp3")
        play(audio_file)

    def _translate(self, audio_data) -> True:
        try:
            text = self.recognizer.recognize_google(audio_data, language = "pt-BR")
            translated = GoogleTranslator(source = "auto", target = "en").translate(text)

            self.display_text.configure(text = text)
            self.display_translated.configure(text = translated)

            self._playAudio(translated)

            return True

        except sr.UnknownValueError:
            raise("Unable to recognize speech")

        except sr.RequestError as e:
            raise("Error: {0}".format(e))
