import time
import phue
from audioplayer import AudioPlayer
import tempocnn


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

# If the app is not registered and the button is not pressed, press the button and rerun connect()
b.connect()

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

#play audio from file "metro.mp3"
AudioPlayer("metro.mp3").play(block=True)