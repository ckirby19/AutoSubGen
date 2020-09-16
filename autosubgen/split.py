import generate
import pyaudio
import speech_recognition as sr
import datetime
import os
from pydub import AudioSegment 
from pydub.silence import split_on_silence
import math
import ffmpeg
import argparse

def silence_based_split(source,silence,threshold,delay,output):
    """
    Input: 
        source - path to video source file
        silence - length of time(ms) that volume must be below threshold for it to be considered silent
        threshold - threshold (in decibels) below average loudness, below which it will be considered silence
        delay - Number of seconds to delay the subtitles by
        output - Name of folder created to store output files
    Output: 
        A file called output with the mp4 audio from the file, the mp4 audio chunks used for speech recognition and the output srt file

    This function works by finding the average loudness of the audio of the input video, and setting a threshold below this average from which the audio will be considered
    silent for that portion. The audio is split at these silent points to make it easier to send the audio to the online speech recognition package. Generate is then called
    on the speech recongition text for each audio chunk 
    """
    os_name = output
    try:
        os.mkdir(os_name)
    except(FileExistsError):
        pass

    output_name = os_name + "/FullAudio.mp3"
    ffmpeg.input(source).output(output_name).run()
    audio = AudioSegment.from_file(output_name)
    audio_rms_dBFS = audio.dBFS #get average loudness of audio
    print("Got Audio, Average Loudness: %s rms" % audio_rms_dBFS)
    
    chunks = []

    chunks = split_on_silence(audio,min_silence_len=silence,silence_thresh=audio_rms_dBFS-threshold)
    num_chunks = len(chunks)
    print("Number of chunks to process: ", num_chunks)

    os.chdir(os_name) 

    current_time = datetime.datetime(100,1,1,0,0,)
    current_time += datetime.timedelta(seconds=delay)
    
    block_num = 1 #srt files start at 1 index
    character_limit = 70 #http://www.permondo.eu/volunteers/introduction-to-subtitling/

    for i in range(num_chunks):
        chunk = chunks[i]
        chunk_silent = AudioSegment.silent(duration=50)

        #Process here created following https://stackoverflow.com/questions/45526996/split-audio-files-using-silence-detection/46001755

        # add 0.5 sec silence to beginning and  
        # end of audio chunk. This is done so that 
        # it doesn't seem abruptly sliced. 
        audio_chunk = chunk_silent + chunk + chunk_silent 
  
        # export audio chunk and save it in  
        # the current directory. specify the bitrate to be 192 k 
        print("saving chunk{0}.wav".format(i)) 
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
  
        # the name of the newly created chunk 
        filename = 'chunk'+str(i)+'.wav'
  
        print("Processing chunk "+str(i)) 
  
        # get the name of the newly created chunk 
        # in the AUDIO_FILE variable for later use. 
        file = filename 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            audio_listened = r.listen(source) 
  
        try: 
            # try converting it to text 
            sentence = r.recognize_google(audio_listened)
            num_characters = len(sentence)
            if num_characters > character_limit:
                print("Long one") #We want to split this into chunks so that words are not cut off but total sentence less than 42 characters
                j=0
                while j<num_characters:
                    new_sentence = sentence[j:j+character_limit]
                    last_space = new_sentence.rfind(' ')
                    if last_space > 1: #If there are spaces in the ting
                        new_sentence = new_sentence[0:last_space] #This will give you a sentence that does not have a word cut off, but is less than character limit
                        j+=last_space+1
                    else:
                        break
                    current_time = generate.generate_srt(new_sentence,block_num,current_time)
                    block_num+=1
                    
            else:
                current_time = generate.generate_srt(sentence,block_num,current_time)
                block_num += 1
            
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 

    os.chdir('..') 