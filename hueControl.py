import time
import phue
import audioplayer

#if file bridgeIp is empty, get bridge ip and store in file
try:
    with open('bridgeIp.txt', 'r') as f:
        if f.read() == '':
            bridgeIp = str(input('Enter bridge ip: '))
            with open('bridgeIp.txt', 'w') as f:
                f.write(bridgeIp)
except:
    print("Err")
    exit(1)

# Connect to the bridge
b = phue.Bridge(bridgeIp)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

#store api key in userId.txt
with open('userId.txt', 'w') as f:
    f.write(b.username)

# Get list of lamp objects and print in terminal
b.get_light_objects('id')
print(b.get_light_objects('id'))

#turn on "Vägglampa 1" at 0x265d800fed0


audioplayer.play('metro.mp3')
bpm = audioplayer.bpm('metro.mp3')

print(bpm)