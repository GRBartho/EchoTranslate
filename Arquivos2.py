from threading import Thread
from time import time
from deep_translator import GoogleTranslator
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        print(sr.Microphone())
        self.microphone = sr.Microphone()
        self.translated = ""
        self.text = ""
        self._continue = True

    def perform(self):
        start_program = time()
        with self.microphone as source:
            while self._continue:
                print("Start listening...")
                # adding time counter
                start = time()
                audio_data = self._listen(source)
                end = time()
                print("Listening ends in : ", end - start)
                print("")

                # Create a new thread for translation
                translate_thread = Thread(
                    target=self._translate, args=(audio_data,))
                translate_thread.start()

        end_program = time()
        print("Program ends in : ", end_program - start_program)

    def _listen(self, source):
        print("")
        self.recognizer.adjust_for_ambient_noise(source)
        audio_data = self.recognizer.record(source, duration=5)
        return audio_data

    def _translate(self, audio_data):
        start = time()
        print("starting translating")
        try:
            text = self.recognizer.recognize_google(
                audio_data, language='pt-BR')
            translated = GoogleTranslator(
                source='auto', target='en'
            ).translate(text)
            self.text = self.text + " " + str(text or "")
            self.translated = self.translated + " " + str(translated or "")
            end = time()

            if "abacaxi" in str(text):
                self._continue = False

            print("Translation ends in : ", end - start)
            print("Original message: ", self.text)
            print("Translated message: ", self.translated)
            print("")

            return True

        except sr.UnknownValueError:
            print("Unable to recognize speech")
        except sr.RequestError as e:
            print("Error: {0}".format(e))


recognizer = SpeechRecognizer()
recognizer.perform()
