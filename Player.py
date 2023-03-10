from os import path
import wave
import numpy as np
import pyaudio
import librosa
import math
import matplotlib.pyplot as plt
import pydub
import AudioConverter

elapsed_time = 0

class Player:
    #constructor
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.bpm = 0
        self.selectAudioFile = ""

    def play_audio_file(self, file_name):
        if file_name == '':
            print("No audio file selected")
            return
        
        else:
            #Convert audio file to .wav
            None
        try:
            print("Playing audio file... \n")
            chunk = 1024
            f = wave.open(file_name, "rb")
            self.stream = self.p.open(format=self.p.get_format_from_width(f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True)
            data = f.readframes(chunk)
            global elapsed_time
            #elapsed_time = 0
            self.stream.start_stream()
            while data:
                current_time = elapsed_time + self.stream.get_time()
                self.stream.write(data)
                data = f.readframes(chunk)
                elapsed_time += len(data) / (f.getframerate() * f.getnchannels() * f.getsampwidth())
            self.stream.stop_stream()
            self.stream.close()
            f.close()
            self.p.terminate()
        except Exception as e:
            print(f"Error playing audio file: {e}")

    def stop_audio_file(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def getAudioPlaying(self):
        return self.stream.is_active()

    def getPlaybackTime(self):
        return int(elapsed_time)

    def getBpm(self, file_name):
        if file_name == "":
            return ""
        else:
            y, sr = librosa.load(file_name)
            #Detect tempo and beats
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            tempo = math.ceil(tempo)
            print(tempo, "BPM")
            return tempo

    def heatSpot(self, file_name):
        if file_name == "":
            return ""
        else:
            #Load the audio file for heatspot detection
            y, sr = librosa.load(file_name)
            #Calculate the spectral flux for each frame of the audio
            spec_flux = librosa.onset.onset_strength(y=y, sr=sr, lag=3, max_size=5)

            #Identify the heatspots by finding the frames with the highest spectral flux values
            # pre_max = number of samples that must be below the threshold before a peak is detected.

            # post_max = number of samples that must be below the threshold after a peak is detected.

            # pre_avg = the number of samples that must be below the average before a peak is detected.

            # post_avg = the number of samples that must be below the average after a peak is detected.

            # delta = a float that specifies the minimum amplitude of the peak in relation to the surrounding samples.

            # wait = an integer that specifies the minimum number of samples between two detected peaks.
            heatspots = librosa.util.peak_pick(spec_flux, pre_max=160, post_max=105, pre_avg=150, post_avg=250, delta=2.0, wait=90)
            heatspots = librosa.frames_to_time(heatspots, sr=sr)
            
            
            #round the heatspots to the nearest second
            for i in range(len(heatspots)):
                heatspots[i] = round(heatspots[i])
            print("Heatspots: ", heatspots, "\n")
            return heatspots