# Auto Generated SRT Files for Videos

This Command-line run Python package creates an SRT subtitle file for a video using Google Online Speech recognition.

For more information about Pythons speech recognition packages, please see the information at https://pypi.org/project/SpeechRecognition/

### Installation

Please run pip install -r requirements.txt to get required modules

### How to run

The following flags are required:
-f or --source [Path to video file] 

The following flags are optional:
-t or --threshold [threshold (in decibels) below average loudness, below which it will be considered silence. default = 20]
-s or --silence [length of time (ms) that volume must be below threshold for it to be considered silent. default = 250]
-d or --delay [Number of seconds to delay the subtitles by. default = 0]
-n or --output [Name of folder created to store output files. default = "output"]

In command line, run `python autosubgen -f /path/to/video` 
Other flags can be used like this: `python autosubgen -f /path/to/video -t 30 -s 100 -d 1.5 -n out`
or like this: `python autosubgen --source /path/to/video --threshold 30 --silence 100 --delay 1.5 --output out`

### How it works

The Google speech recognition online software is used to generate text from a video by first extracting the audio from the video, splitting the audio into smaller chunks based on where
there is silence in the audio and sending each chunk to the cloud to extract the text. Smaller chunks are needed to improve accuracy and to make it easier to send to the cloud. 
Once the text is extracted, the 

The generated text, and the timings for the audio, are not completely accurate and the accuracy diminishes if the source video contains noise other than the desired audio. This Python package simply creates a good starting point from which subtitles can be improved. 

Once the SRT file is generated, ffmpeg or other video editing software can be used to combine the subtitles with the video. For ffmpeg, see here: https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo

### Why create it?

Subtitles should be available for all videos to allow those with hearing related disabilities to have equal access to information online
