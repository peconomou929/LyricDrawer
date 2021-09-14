import os 
import sys
import argparse

parser = argparse.ArgumentParser(description = "Draw the lyrics from the specified input file.")
parser.add_argument("inputfile")
parser.add_argument("-l", "--lyricsize", default = 11, type = int, help = "The font size of the lyrics; an integer between 5 and 36 inclusive.")
parser.add_argument("-s", "--spacing", default = 4, type = int, help = "The spacing between objects in the document; a non-negative integer.")
args = parser.parse_args()

from code import document 

if args.lyricsize not in range(5, 36 + 1):
	print("The lyric size must be between 5 and 36 inclusive.")
	sys.exit()

doc = document.LyricDocument(args.inputfile)
doc.draw(lyric_size = args.lyricsize, spacing = args.spacing)
new_file_path = doc.target

os.system("open " + new_file_path)
