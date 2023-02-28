import tkinter as tk;
from tkinter import filedialog
from hueControl import hueControl;
from Player import Player;
import threading;

player = Player()
selectedLamps = []

def selectAudioFile():
    root = tk.Tk()
    root.withdraw()
    #sets this class' filepath attribute to the selected file
    global filepath
    global player
    global t
    filepath = filedialog.askopenfilename()
    print(filepath)
    t = threading.Thread(target=player.play_audio_file, args=(str(filepath),))

def main():
    hue = hueControl()
    player = Player()
    #print(player.heatSpot(filepath))
    

    #exec def connect in hueControl
    hue.connect()

    lightarr = hue.selectLights()

    #make the window
    window = tk.Tk()
    window.title("Hue Me")
    window.geometry("600x600")
        

    #make select song button
    selectSongButton = tk.Button(window, text="Select Song", command=selectAudioFile)
    selectSongButton.pack()
    
    #make play button
    playButton = tk.Button(window, text="Play", command=t.start)
    playButton.pack()

    #make quit button
    stopButton = tk.Button(window, text="Quit (double click)", command=player.stop_audio_file)
    stopButton.pack()
    
    

    #make bpm label
    bpmLabel = tk.Label(window, text="BPM: " + str(player.getBpm(filepath)))
    bpmLabel.pack()

    #make lamp selector that shows all the lamps from lightarr
    lampSelector = tk.Listbox(window)
    lampSelector.pack()
    for light in lightarr:
        lampSelector.insert(tk.END, light)

    #check what lamps are selected and set them to the selected lamps
    
    def selectLamp(event):
        selectedLamps.append(lampSelector.get(lampSelector.curselection()))
        print(selectedLamps)
    lampSelector.bind("<<ListboxSelect>>", selectLamp)

    #Start the visuals when something is selected and the play button is pressed
    def startVisuals():
        global filepath
        print("Visuals starting...",filepath)
        if (t.is_alive() == True and len(selectedLamps) > 0):
            print("Visuals started")
            hue.randomColorShow(selectedLamps, player.getBpm(filepath), player.heatSpot(filepath))
        else:
            print("Visuals not started")
    

    #make visualizer button
    visualizerButton = tk.Button(window, text="Visualizer", command=startVisuals)
    visualizerButton.pack()

    # make a label for playback time and update every frame
    timeLabel = tk.Label(window, text="Time: " + str(0))
    timeLabel.pack()

    # update every frame
    def update():
        #print("Time: ", int(player.getPlaybackTime()))
        timeLabel.config(text="Time: " + str(player.getPlaybackTime()))

        # start the update loop
        window.after(1, update)

    # start the update loop
    window.after(1, update)

    # pack the window
    window.mainloop()


if __name__ == "__main__":
    selectAudioFile()
    main()