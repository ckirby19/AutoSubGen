import math
import datetime

def generate_srt(sentence_to_parse,block_num,current_time):
    """
    Input: 
    sentence_to_parse - generated text from audio chunk is split into sentences of max 70 characters
    block_num - SRT files require numbers above each section of text
    current_time - start time of current sentence 

    Output:
    end_time - end time of current sentence (therefore current_time for next sentence)

    
    Take the generated text and write to output srt file
    """

    num_words = len(sentence_to_parse.split())
    time_add = len(sentence_to_parse.split())*0.36 #0.36 found empirically as average number of seconds per word for this audio
    ##TODO write function to find average number of seconds per word for input audio file  
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