import wave
import pyaudio
import librosa
import math
import threading;


class Player:

    #constructor
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        isActive = self.stream.is_active()
        self.bpm = 0
        self.selectAudioFile = ""
    
    
    def play_audio_file(self, file_name):
        if file_name == '':
            print("No audio file selected")
            return
        print("Playing audio file... \n")
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

    def stop_audio_file(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def getAudioPlaying(self):
        return self.stream.is_active()
    
    
    
    def getBpm(self, file_name):
        if file_name == "":
            return ""
        else:
            print("Loading audio file for BPM scan... \n")
            y, sr = librosa.load(file_name)
            print(file_name)
            #Detect tempo and beats
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            tempo = math.ceil(tempo)

            #Print estimated tempo
            print("Estimated tempo: ", tempo, " BPM \n")
            return tempo