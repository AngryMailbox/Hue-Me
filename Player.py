import wave
import pyaudio


class Player:
    #constructor
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        isActive = self.stream.is_active()
    
    #play audio file
    def play_audio_file(self, file_name):
        chunk = 1024
        f = wave.open(file_name, "rb")
        self.stream = self.p.open(format=self.p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)
        while data:
            self.stream.write(data)
            data = f.readframes(chunk)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def audioPlaying(self):
        return self.stream.is_active()