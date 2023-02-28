import math
import time
import phue
import threading
import random
from rgbxy import Converter
from Player import Player

converter = Converter()

#sound file
sound = "stamp.wav"

class hueControl:

    #constructor
    def __init__(self):
        self.bridgeIp = ''
        self.userId = ''
        self.b = ''

    def connect(self): #if file bridgeIp is empty, get bridge ip and store in file
        try:
            with open('bridgeIp.txt', 'r') as f:
                if f.read() == '':
                    self.bridgeIp = str(input('Enter bridge ip: '))
                    with open('bridgeIp.txt', 'w') as f:
                        f.write(self.bridgeIp)
                else:
                    with open('bridgeIp.txt', 'r') as f:
                        self.bridgeIp = f.read()
        except:
            print("Err")
            exit(1)
        b = phue.Bridge(self.bridgeIp) # Connect to the bridge
        try: # If the app is not registered the app must be rerun in order to register the app with the bridge
            b.connect()
        except:
            print("Press the button on the bridge and rerun the program")
            exit(1)
        b.get_api() # Get the bridge state (returns full dictionary)
        with open('userId.txt', 'w') as f: #store api key in userId.txt
            f.write(b.username)

    

    def selectLights(self):
        b = phue.Bridge(self.bridgeIp)
        lampor = b.get_light_objects('name')
        #lampor = {'Vägglampa 1': lampor['Vägglampa 1'], 'Vägglampa 2': lampor['Vägglampa 2'], 'Vägglampa 3': lampor['Vägglampa 3']}
        return lampor


    def setLight(lightarr, xbright,xcolor):
        for light in lightarr:
            lightarr[light].brightness = xbright
            lightarr[light].xy = xcolor


    def randomColorShow(self, lampor, tempo):
        for light in lampor:
            newlightarr = {light: lampor[light]}
        try:
            while True:
                bri = random.randint(100, 254)
                tempoChange = random.randint(1, 2)
                hueControl.setLight(newlightarr, bri, converter.get_random_xy_color())
                time.sleep(60/(tempo*tempoChange))
                if not Player.getAudioPlaying():
                    break
        except:
            print("lights turned off")