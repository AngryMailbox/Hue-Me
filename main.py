import tkinter as tk;
from tkinter import END, filedialog
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

def stopAudioFile():
    player.stop_audio_file()

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
    stopButton = tk.Button(window, text="Exit", command=stopAudioFile)
    stopButton.pack()
    
    

    #make bpm label
    bpmLabel = tk.Label(window, text="BPM: " + str(player.getBpm(filepath)))
    bpmLabel.pack()

    #make lamp selector that shows all the lamps from lightarr
    lampSelector = tk.Listbox(window, selectmode=tk.MULTIPLE)
    #remove underlining of font from selected items
    for light in lightarr:
        lampSelector.insert(tk.END, light)
    lampSelector.config(height=15)
    lampSelector.pack()
    
    #check what lamps are selected and set them to the selected lamps
    def selectLamp(event):
        #append only if it's not already in the list
        try:
            if lampSelector.get(lampSelector.curselection()) not in selectedLamps:
                selectedLamps.append(lampSelector.get(lampSelector.curselection()))
                lampSelector.itemconfig(lampSelector.curselection(), bg="green")
            else:
                selectedLamps.remove(lampSelector.get(lampSelector.curselection()))
                lampSelector.itemconfig(lampSelector.curselection(), bg="white")
            print(selectedLamps)
            lampSelector.selection_clear(0,END)
            lampSelector.activate(lampSelector.curselection())
        except:
            None
    lampSelector.bind("<<ListboxSelect>>", selectLamp)

    #Start the visuals when something is selected and the play button is pressed
    def startVisuals():
        global filepath
        if (t.is_alive() == True and len(selectedLamps) > 0):
            a = threading.Thread(target=hue.randomColorShow, args=(selectedLamps, player.getBpm(filepath), player.heatSpot(filepath)))
            a.start()
        else:
            print("Err: Visuals not started")
    

    def startStrobe():
        global filepath
        if (t.is_alive() == True and len(selectedLamps) > 0):
            a = threading.Thread(target=hue.strobe, args=(selectedLamps, player.getBpm(filepath)))
            a.start()
        else:
            print("Err: Visuals not started")

    #make visualizer button
    visualizerButton = tk.Button(window, text="Visualizer", command=startVisuals)
    visualizerButton.pack()

    # make a label for playback time and update every frame
    timeLabel = tk.Label(window, text="Time: " + str(0))
    timeLabel.pack()

    # Start strobe
    strobeButton = tk.Button(window, text="Strobe", command=startStrobe)
    strobeButton.pack()

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