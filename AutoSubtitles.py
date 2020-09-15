import pyaudio
import speech_recognition as sr
import datetime
import os
from pydub import AudioSegment 
from pydub.silence import split_on_silence
import math
import ffmpeg
import argparse

ap = argparse.ArgumentParser()
#must add short hand and long hand versions of flag 
ap.add_argument("-f", "--filepath", type=str,required=True,
	help="path to directory containing video") #then can then be accessed using args["filepath"]
ap.add_argument("-t","--threshold",type=int,default=20,
    help="threshold (in decibels) below average loudness, below which it will be considered silence")
ap.add_argument("-s","--silence",type=int,default=250,
    help="length of time(ms) that volume must be below threshold for it to be considered silent")
ap.add_argument("-d","--delay",type=float,default=0,
    help="Number of seconds to delay the subtitles by")
ap.add_argument("-n","--filename",type=str,default="output",
    help="Name of folder created to store output files")
args = vars(ap.parse_args())

def silence_based_split():
    """
    

    """
    os_name = args["filename"]
    try:
        os.mkdir(os_name)
    except(FileExistsError):
        pass

    output_name = os_name + "/FullAudio.mp3"
    ffmpeg.input(args["filepath"]).output(output_name).run()
    audio = AudioSegment.from_file(output_name)
    audio_rms_dBFS = audio.dBFS
    print("Got Audio, Stats: %s rms" % audio_rms_dBFS)
    
    chunks = []

    chunks = split_on_silence(audio,min_silence_len=args["silence"],silence_thresh=audio_rms_dBFS-args["threshold"])
    num_chunks = len(chunks)
    print("Number of chunks to process: ", num_chunks)

    os.chdir(os_name) 

    current_time = datetime.datetime(100,1,1,0,0,)
    current_time += datetime.timedelta(seconds=args["delay"])
    
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
                    current_time = generate_srt(new_sentence,block_num,current_time)
                    block_num+=1
                    
            else:
                current_time = generate_srt(sentence,block_num,current_time)
                block_num += 1
            
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 

    os.chdir('..') 

def generate_srt(sentence_to_parse,block_num,current_time):

    num_words = len(sentence_to_parse.split())
    time_add = len(sentence_to_parse.split())*0.36 #0.36 found empirically as number of seconds per word on average for this audio
    frac,whole = math.modf(time_add)
    whole = int(whole)
    frac = int(round(frac,2) * 1000000) 
    end_time = current_time + datetime.timedelta(0,whole,frac)
    
    str_current_time = str(current_time.time())
    str_end_time = str(end_time.time())

    with open("Textblocks.srt","a") as fh:
        fh.write(str(block_num))
        fh.write("\n")
        fh.write(str_current_time[:8])
        fh.write(",")
        if str_current_time[9:12] == "":
            fh.write("000")
        else:
            fh.write(str_current_time[9:12])
        fh.write(" --> ")
        fh.write(str_end_time[:8])
        fh.write(",")
        if str_end_time[9:12] == "":
            fh.write("000")
        else:
            fh.write(str_end_time[9:12])
        fh.write("\n")
        fh.write(sentence_to_parse)
        fh.write("\n")
        fh.write("\n")

    return end_time

if __name__ == '__main__': 
    silence_based_split() 