import sys


def getInputFile():
    if(len(sys.argv) <= 1):
        print("ERROR: Please enter path to XML dump!")
        exit()
    return sys.argv[1]
