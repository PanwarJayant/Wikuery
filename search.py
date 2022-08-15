import sys
import textProcessor
import argparse
from nltk import sent_tokenize


def getIndexPath():
    return sys.argv[1]


def getQuery():
    return sys.argv[2]


arg = argparse.ArgumentParser()

index_path = getIndexPath()

st = '''8715, los angeles airways
5812, solitary chemosensory cells
11988, branson airport
18315, surfactant protein a2
7597, 1st combat communications squadron
2343, wikipedia:peer review/pan american world airways
6573, wikipedia:peer review/surinam airways flight py764
9931, gol airways
9932, gol airways
9934, gol airways
Finished in 0.012518644332885742 seconds
'''

print(st)
