from asyncio.windows_events import NULL
from email.policy import default
from os import link
from turtle import title
from unicodedata import category
import xml.sax
# import parser
from handler import *
from collections import defaultdict


def intializeDicts():
    return defaultdict(int)


def updateComponents(component, dict):
    words_set.update(component)
    for part in component:
        dict[part] += 1


def createIndex():
    return NULL


words_set = set()
title_dict = intializeDicts()
body_dict = intializeDicts()
category_dict = intializeDicts()
infobox_dict = intializeDicts()
link_dict = intializeDicts()
reference_dict = intializeDicts()

input_file = getInputFile()
