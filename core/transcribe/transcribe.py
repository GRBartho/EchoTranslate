import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator

class Transcribe:
    def __init__(self):
        # Configura o modelo de linguagem para modelo médio e lingua inglesa
        self.model = whisper.load_model("base")

    def audio_to_text(self, filename, language='pt'):
        # Transcreve o áudio para texto
        result = self.model.transcribe(filename, fp16=False, language=language)
        return result["text"]
    
    def text_to_audio(self, text, filename, language='en'):
        myobj = gTTS(text=text, lang=language, slow=True)
        myobj.save(filename)
        return filename
    
    def translate(self, text, language='en'):
        return GoogleTranslator(
            source='auto', target=language
        ).translate(text)