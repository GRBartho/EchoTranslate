import whisper
import pyaudio
import wave
import os
from gtts import gTTS
from deep_translator import GoogleTranslator

def listenToAudio():
    # Configura o modelo de linguagem para modelo médio e lingua inglesa
    model = whisper.load_model("medium.en")
    # Transcreve o áudio para texto
    result = model.transcribe("output.wav", fp16=False, language="pt")
    # Retorna o texto transcrito
    return result["text"]


def listenMic():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    seconds = 3

    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("* end of recording")

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def playAudio(text):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")


def getWordToSearch():
    # Recebe a palavra que deseja buscar no áudio
    word = input("Insira a palavra que deseja buscar no áudio: ")
    # Retorna a palavra
    return word


""" def openFile():
    # Escolhe nome para o novo arquivo
    newFile = input(
        "Insira o nome do novo arquivo que guardará o conteúdo do áudio: ")
    # Usa a função open para abrir o novo arquivo com w+ para escrita.
    with open(newFile+".txt", "w+") as file:
        # Escreve o conteúdo do áudio no arquivo
        word = getWordToSearch()
        # Recebe o texto transcrito do áudio
        audioText = listenToAudio()
        # Conta quantas vezes a palavra aparece no áudio
        wordQuantity = audioText.lower().count(word.lower())
        # Verifica se a palavra foi encontrada no áudio, caso sim, mostra quantas vezes, se não, mostra que não foi encontrada
        if word.lower() in audioText.lower():
            print("\nA palavra ", word, " foi encontrada no áudio ",
                  wordQuantity, " vezes \n")
        else:
            print("\nA palavra ", word, " não foi encontrada no áudio \n")
        # Escreve o conteúdo do áudio no arquivo
        file.write(audioText)
        print("Arquivo criado com sucesso!!")
        print("Conteúdo do arquivo: ")
        print("\n")
        # Volta o cursor para o início do arquivo e lê o conteúdo
        file.seek(0, 0)
        print(file.read())
        print("\n")
        print("Nome do arquivo: ", newFile) """


def main():
    listenMic()
    text = listenToAudio()
    translatedText = GoogleTranslator(
        source="auto", target="en").translate(text)
    playAudio(translatedText)
    print("\n")
    print(translatedText)


main()
