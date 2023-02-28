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
    

    #exec def connect in hueControl
    hue.connect()

    lightarr = hue.selectLights()

    #make the window
    window = tk.Tk()
    window.title("Hue Controller")
    window.geometry("600x600")

    #make start visuals button
    startVisualsButton = tk.Button(window, text="Start Visuals", command=hue.randomColorShow(lightarr, player.getBpm(filepath)))
    startVisualsButton.pack()
        

    #make select song button
    selectSongButton = tk.Button(window, text="Select Song", command=selectAudioFile)
    selectSongButton.pack()
    
    #make play button
    playButton = tk.Button(window, text="Play", command=t.start)
    playButton.pack()

    #make stop button
    stopButton = tk.Button(window, text="Stop", command=player.stop_audio_file)
    stopButton.pack()

    #make quit button
    quitButton = tk.Button(window, text="Quit", command=quit)
    quitButton.pack()
    

    #make bpm label and update it every second
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


    #pack the window
    window.mainloop()





if __name__ == "__main__":
    selectAudioFile()
    main()