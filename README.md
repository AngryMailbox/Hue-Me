# Hue-Me

A project that aims to revolutionize music sync-effects with close-to-zero delay for Philips hue and other Zigbee-compatible devices.

## Introduction

The Zigbee Music Sync project is designed to enhance the music experience by synchronizing the music with Philips Hue and other Zigbee-compatible devices. The project allows you to create close-to-zero delay music sync-effects that create an immersive audio-visual experience. 

## Requirements

To run the project, you will need to install the following dependencies:

* Python <=3.7
* The `requirements.txt` file included in the repository

You can install the dependencies by running the following command:

pip install -r requirements.txt

## Files

The repository contains the following files:

* `Player.py`: A Python module that handles audio playback using the PyAudio library
* `hueControl.py`: A Python module that handles the communication with the Philips Hue bridge and the Zigbee devices
* `*.wav`: Example audio files used to test the project
* `main.py`: The main Python script that runs the project
* `requirements.txt`: A text file that lists the dependencies required to run the project

## Usage

To use the project, you can run the `main.py` script with the following command:

python main.py

After prompting for The script will start playing a .wav file of your choice and you can start synchronizing the lights with the music. For now, you can adjust different light modes by editing the `main.py` file.

## Contribution

Contributions to the project are welcome. You can create a pull request or open an issue to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
