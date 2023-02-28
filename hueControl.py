import math
import time
import phue
import threading
import librosa
import random
from rgbxy import Converter
from Player import Player
converter = Converter()

sound = "stamp.wav"





#if file bridgeIp is empty, get bridge ip and store in file
try:
    with open('bridgeIp.txt', 'r') as f:
        if f.read() == '':
            bridgeIp = str(input('Enter bridge ip: '))
            with open('bridgeIp.txt', 'w') as f:
                f.write(bridgeIp)
        else:
            with open('bridgeIp.txt', 'r') as f:
                bridgeIp = f.read()
except:
    print("Err")
    exit(1)

# Connect to the bridge
b = phue.Bridge(''+bridgeIp)

# If the app is not registered the app must be rerun in order to register the app with the bridge
try:
    b.connect()
except:
    print("Press the button on the bridge and rerun the program")
    exit(1)

# Get the bridge state (returns full dictionary)
b.get_api()

#store api key in userId.txt
with open('userId.txt', 'w') as f:
    f.write(b.username)

# Get list of lamp objects
#b.get_light_objects('id')

# Get lamp object
lampor = b.get_light_objects('name')

# Choose 'Vägglampa 1' lamp to use and put in a new array
#lampor = {'Vägglampa 1': testlampa['Vägglampa 1']}
# Choose 'Vägglampa 1', 'Vägglampa 2' lamps to use and put in a new array
lampor = {'Vägglampa 1': lampor['Vägglampa 1'], 'Vägglampa 2': lampor['Vägglampa 2'], 'Vägglampa 3': lampor['Vägglampa 3']}

for light in lampor:
    lampor[light].on = True 


def setLight(lightarr, xbright,xcolor):
    for light in lightarr:
        lightarr[light].brightness = xbright
        lightarr[light].xy = xcolor


#Load audio file
y, sr = librosa.load(sound)

#Detect tempo and beats
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

#Print estimated tempo
print("Estimated tempo: ", tempo, " BPM")
tempo = math.ceil(tempo)


#play audio file in multithreading
player = Player()
t = threading.Thread(target=player.play_audio_file, args=(sound,))
t.start()

#blink light at tempo
try:
    while True:
        bri = random.randint(100, 254)
        tempoChange = random.randint(1, 2)
        setLight(lampor, bri, converter.get_random_xy_color())
        time.sleep(60/(tempo*tempoChange))
        if not player.audioPlaying():
            exit()

#if keyboard interrupt, turn off light and exit
except KeyboardInterrupt:
    b.set_light('Vägglampa 1', 'on', False)
    exit()