import split
import argparse

ap = argparse.ArgumentParser()
#must add short hand and long hand versions of flag 
ap.add_argument("-f", "--source", type=str,required=True,
	help="path to directory containing video") #then can then be accessed using args["sourcepath"]
ap.add_argument("-s","--silence",type=int,default=250,
    help="length of time(ms) that volume must be below threshold for it to be considered silent")
ap.add_argument("-t","--threshold",type=int,default=20,
    help="threshold (in decibels) below average loudness, below which it will be considered silence")
ap.add_argument("-d","--delay",type=float,default=0,
    help="Number of seconds to delay the subtitles by")
ap.add_argument("-n","--output",type=str,default="output",
    help="Name of folder created to store output files")
args = vars(ap.parse_args())

if __name__ == "__main__":
    split.silence_based_split(args["source"],args["silence"],args["threshold"],args["delay"],args["output"])