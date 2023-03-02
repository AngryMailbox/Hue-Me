import math
import time
import librosa
import phue
import threading
import random
from rgbxy import Converter
from Player import Player

converter = Converter()

#sound file
sound = "stamp.wav"
lightarr = []

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
        global lightarr
        lightarr = lampor
        #lampor = {'Vägglampa 1': lampor['Vägglampa 1'], 'Vägglampa 2': lampor['Vägglampa 2'], 'Vägglampa 3': lampor['Vägglampa 3']}
        return lampor

    def setLight(lampor, xbright, xcolor, xtrans):
        for light in lampor:
            lightarr[light].brightness = xbright
            lightarr[light].transitiontime = xtrans
            lightarr[light].xy = xcolor

    def randomColorShow(self, lampor, tempo, heatspots):
        while True:
            hueControl.syncedColorShow(heatspots, lampor)
            bri = random.randint(100, 254)
            tempoChange = random.randint(1, 2)
            xtrans = random.randint(1, 5)
            hueControl.setLight(lampor, bri, converter.get_random_xy_color(), xtrans)
            time.sleep(60/(tempo*tempoChange))

    def threadedRandomColorShow(self, lampor, tempo, heatspots):
        # Create a thread for each light
        threads = []
        for light in lampor:
            lightarr = []
            lightarr.append(light)
            t = threading.Thread(target=hueControl.randomColorShow, args=(self, lightarr, tempo, heatspots))
            threads.append(t)
            t.start()

    def strobe(self, lampor, tempo):
        while True:
            hueControl.setLight(lampor, 254, converter.hex_to_xy('ffffff'), 0)
            time.sleep(15/tempo)
            hueControl.setLight(lampor, 0, converter.hex_to_xy('ffffff'), 0)
            time.sleep(30/tempo)
    
    def syncedColorShow(heatspots, lampor):
        for heatspot in heatspots:
            heatspot = round(heatspot)
            if Player.getPlaybackTime(0)+1 == int(heatspot):
                for light in lampor:
                    lightarr[light].brightness = 255
                    time.sleep(0.1)
                    lightarr[light].transitiontime = 0
                    lightarr[light].xy = converter.hex_to_xy('ffffff')
                    time.sleep(0.1)
                    lightarr[light].brightness = 100
                    lightarr[light].xy = converter.hex_to_xy('a020f0')
                    time.sleep(0.1)
                    lightarr[light].brightness = 255