import time
import phue
from audioplayer import AudioPlayer
import librosa
import numpy
#import tempocnn


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
b.get_light_objects('id')
print(b.get_light_objects('id'))

#turns on "Vägglampa 1"
b.set_light('Vägglampa 1', 'on', True)

#plays audio from "metro.mp3"
AudioPlayer("metro.mp3").play(block=True)

y, sr = librosa.load("metro.mp3")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print("Estimated tempo: {:.2f} BPM".format(tempo))

#blink light at tempo
try:
    while True:
        b.set_light('Vägglampa 1', 'on', True)
        print("on")
        time.sleep(60/tempo)
        b.set_light('Vägglampa 1', 'on', False)
        print("off")
        time.sleep(60/tempo)
#if keyboard interrupt, turn off light and exit
except:
    b.set_light('Vägglampa 1', 'on', False)

exit()