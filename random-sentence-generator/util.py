"""
File: util.py
Author: Alex Gill
A utility file for the random sentence generator program.
"""
import pathlib

def readfile(filename, args=None):
    """
    Reads a file of words.
    Param filename: The file name
    Param args: The dictionary keys, if creating dictionaries
    Return: A tuple of the words.
    """
    # Open the file
    path = str(pathlib.Path(__file__).parent.resolve()) + '/' + filename
    inputfile = open(path, 'r')

    # Read the words...
    words = []
    # ...into lists
    if args == None:
        for line in inputfile:
            word = []
            tokens = line.strip().split('/')
            if len(tokens) == 1:
                words.append(tokens[0])
            else:
                for i in range(len(tokens)):
                    word.append(tokens[i])
                words.append(word)
    # ...into dictionaries
    else:
        for line in inputfile:
            word = {}
            tokens = line.strip().split('/')
            if len(tokens) == 1:
                words.append(tokens[0])
            else:
                for i in range(len(tokens)):
                    word[args[i]] = tokens[i]
                words.append(word)

    # Close the file
    inputfile.close()

    # Return the words
    return tuple(words)