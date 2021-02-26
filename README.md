# crossword
This repository contains the Python program I developed to generate an American crossword puzzle given a set of pre-existing conditions (dimensions for the puzzle, number of blanks/black grid spots, and any characters required in grid spots). The puzzle must have rotational symmetry and letters must form a word both horizontally and vertically. This program can be run through the command line (python xwordanticlump.py dimensions number_of_blanks words_text_file grid_spot_and_required_character) and will first display the puzzle with the required characters, then the puzzle with all the black grid spots with the required characters filled in, and then the filled-in puzzle itself. 

Ex. 
python xwordanticlump.py 9x13 19 dctLarge.txt "v2x3#" "v1x8#" "h3x1#" "v4x5##"
