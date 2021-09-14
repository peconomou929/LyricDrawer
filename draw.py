import os 
import argparse

parser = argparse.ArgumentParser(description = "Draw the lyrics from the specified input file.")
parser.add_argument("inputfile")
parser.add_argument("-l", "--lyricsize", default = 11, help = "The font size of the lyrics; an integer between 5 and 36 inclusive.")
parser.add_argument("-m", "--margin", default = 4, help = "The spacing between objects in the document; a non-negative integer.")
args = parser.parse_args()

from code import document 

doc = document.LyricDocument(args.inputfile)
doc.draw(lyric_size = args.lyricsize, margin = args.margin)
new_file_path = doc.target

os.system("open " + new_file_path)
