# Auto Generated SRT Files for Videos

This Command-line run Python package creates an SRT subtitle file for a video using Google Online Speech recognition.

For more information about Pythons speech recognition packages, please see the information at https://pypi.org/project/SpeechRecognition/

### Installation

Please run XXX

### Use

The following flags are required:
-f or --filepath [Path to video file] 
The following flags are optional:
-t or --threshold [threshold (in decibels) below average loudness, below which it will be considered silence]
-s or --silence [length of time(ms) that volume must be below threshold for it to be considered silent]
-d or --delay [Number of seconds to delay the subtitles by]
-n or --filename [Name of folder created to store output files]

In command line, run python auto-sub-gen.py -f /path/to/video 

### How it works
