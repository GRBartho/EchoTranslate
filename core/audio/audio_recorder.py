import pyaudio
import wave


class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.audio = None
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.callback
        )
        self.stream.start_stream()

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def save_recording(self, filename):
        wf = wave.open(filename, "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()
